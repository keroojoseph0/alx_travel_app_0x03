from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('listing', views.ListingViewsets)
router.register('booking', views.BookingViewsets)

app_name = 'listing'

urlpatterns = [
    path('', include(router.urls)),
    path('payments/<int:booking_id>/', views.initiate_payment, name = 'initiate_payment'),
    path('payments/verify/', views.verify_payment, name='verify-payment'),
]
