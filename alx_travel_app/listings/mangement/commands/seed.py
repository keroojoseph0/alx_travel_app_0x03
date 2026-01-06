from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth.models import User
from faker import Faker
import random
from django.utils import timezone

fake = Faker()

class Command(BaseCommand):
    help = "Seed the database with listings (Django 5 compatible)"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR("Create at least 1 user first"))
            return

        Listing.objects.all().delete()  # clear old listings

        for _ in range(10):
            Listing.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.text(),
                price_per_night=round(random.uniform(50, 500), 2),
                address=fake.address(),
                owner=random.choice(users),
                created_at=timezone.now(),
                updated_at=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))
