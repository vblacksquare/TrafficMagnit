import csv
import os
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from currency.models import CurrencyChoices, CurrencyRate

class Command(BaseCommand):
    help = 'Creates csv file for currency tracking'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            default='currency_rates.csv',
        )

    def handle(self, *args, **options):
        filename = options['name']
        file_path = os.path.join(settings.BASE_DIR, filename)

        header = ['A', "B", "Buy", "Sell"]

        try:
            with open(file_path, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)

                response = requests.get(url="http://127.0.0.1:8000/api/rates/")
                currencies = response.json()

                for item in currencies:
                    writer.writerow([
                        item["currency_a"],
                        item["currency_b"],
                        item["rate_buy"],
                        item["rate_sell"]
                    ])

            self.stdout.write(self.style.SUCCESS(f'File created: {file_path}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating file: {e}'))
