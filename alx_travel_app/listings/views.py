from celery import shared_task
from django.shortcuts import get_object_or_404, render
from .models import Listing, Booking, Review, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings
import requests
from .tasks import send_payment_success_email, send_booking_confirmation_email


# Create your views here.

class ListingViewsets(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    
class BookingViewsets(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        send_booking_confirmation_email.delay(
            booking.user.email,
            booking.id
        )
        


@api_view(['POST'])
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, pk = booking_id)

    payment = Payment.objects.create(
        booking = booking,
        amount = booking.total_price,
    )

    headers = {
        'Autherization': f'Bearer {settings.CHAPA_SECRET_KEY}',
        'Content-Type': 'application/json'
    }


    payload = {
        "amount": str(payment.amount),
        "currency": "ETB",
        "email": booking.user.email,
        "first_name": booking.user.first_name,
        "last_name": booking.user.last_name,
        "tx_ref": str(payment.reference),
        "callback_url": "http://localhost:8000/api/payments/verify/",
        "return_url": "http://localhost:3000/payment-success",
        "customization": {
            "title": "Travel Booking",
            "description": "Payment for booking",
        },
    }

    response = requests.post(
        f"{settings.CHAPA_BASE_URL}/transaction/initialize",
        json=payload,
        headers=headers,
    )

    data = response.json()

    if data.get("status") == "success":
        payment.transaction_id = data["data"]["tx_ref"]
        payment.save()

        return Response({
            "checkout_url": data["data"]["checkout_url"]
        })

    payment.status = "FAILED"
    payment.save()

    return Response({"error": "Payment initiation failed"}, status=400)

    
@api_view(["GET"])
def verify_payment(request):
    tx_ref = request.query_params.get("tx_ref")

    payment = Payment.objects.get(reference=tx_ref)

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    response = requests.get(
        f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}",
        headers=headers
    )

    data = response.json()

    if data["status"] == "success" and data["data"]["status"] == "success":
        payment.status = "COMPLETED"
        payment.save()

        send_payment_success_email.delay(payment.booking.user.email)

        return Response({"message": "Payment verified successfully"})

    payment.status = "FAILED"
    payment.save()

    return Response({"message": "Payment failed"}, status=400)


