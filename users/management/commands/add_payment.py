from django.core.management.base import BaseCommand
from users.models import Payment


class Command(BaseCommand):
    help = "Add payment to the database"

    def handle(self, payments=None, *args, **options):
        payment, _ = Payment.objects.get_or_create(
            user="Anonim",
            payment_date="27.07.2025",
            paid_course="Course-1",
            paid_lesson="Lesson-1",
            payment_amount="1000",
            payment_method="BANK_TRANSFER",
        )
        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(self.style.SUCCESS
                                  ("Successfully added payment!"))
            else:
                self.stdout.write(self.style.WARNING
                                  ("Payment already exist!"))
