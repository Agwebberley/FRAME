# Management Command to generate fake data for 'Part.part' model

import random
from django.core.management.base import BaseCommand
from faker import Faker
from frame_template.part.models import Part


class Command(BaseCommand):
    help = "Generate fake data for Part model"

    def add_arguments(self, parser):
        parser.add_argument(
            "total", type=int, help="Indicates the number of fake data to be generated"
        )

    def handle(self, *args, **kwargs):
        total = kwargs["total"]
        fake = Faker()
        for _ in range(total):
            part = Part(
                name=fake.name(),
                description=fake.text(),
                price=fake.random_int(min=1, max=1000),
                stock_quantity=fake.random_int(min=1, max=1000),
            )
            part.save()
        self.stdout.write(
            self.style.SUCCESS(f"{total} fake data created successfully!")
        )
