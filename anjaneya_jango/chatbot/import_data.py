# import_data.py

import csv
from django.core.management.base import BaseCommand
from chatbot.models import Destination  # Import your Destination model


class Command(BaseCommand):
    help = 'Import data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                destination = Destination(
                    city=row['city'],
                    place=row['place'],
                    ratings=float(row['ratings']),
                    distance=float(row['distance']),
                    place_desc=row['place_desc']
                )
                destination.save()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
