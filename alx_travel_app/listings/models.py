from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxLengthValidator
import uuid
# Create your models here.

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=7, decimal_places=2)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='listings', on_delete=models.CASCADE)

    def __str__(self):
         return self.title
    
    
# pending, confirmed, cancelled

class Status(models.TextChoices):
        pending = 'Pending'
        confirmed = 'Confirmed'
        cancelled = 'Cancelled'
    
    
class Booking(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status, default=Status.pending)
    listing = models.ForeignKey(Listing, related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)

    
class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MinValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()


class Payment(models.Model):
    reference = models.UUIDField(default=uuid.uuid4, unique=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # 10-000-000.00
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status, default=Status.pending)

    def __str__(self):
        return (f"{self.reference} - {self.status}")

