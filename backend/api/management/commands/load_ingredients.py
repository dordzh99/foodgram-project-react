import csv
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import json and csv files into database'

    def handle(self, *args, **options):
        with open(
            f'{settings.BASE_DIR}/data/ingredients.csv',
            'r',
            encoding='utf-8'
        ) as csv_file:
            csv_data = csv.reader(csv_file)
            Ingredient.objects.bulk_create(
                Ingredient(name=row[0], measurement_unit=row[1])
                for row in csv_data
            )

        with open(
            f'{settings.BASE_DIR}/data/ingredients.json',
            'r',
            encoding='utf-8'
        ) as json_file:
            json_data = json.load(json_file)
            for item in json_data:
                Ingredient.objects.create(
                    name=item['name'],
                    measurement_unit=item['measurement_unit']
                )
        self.stdout.write(self.style.SUCCESS(
            'Успешно выгружены данные с csv и json файла'
          
