
import requests
from django.utils import timezone
import datetime
from celery import shared_task
from .models import CurrencyRate


@shared_task
def fetch_currency_rates():
    url = "https://api.monobank.ua/bank/currency"
    response = requests.get(url)

    if response.status_code != 200:
        print(response.text)
        return

    data = response.json()

    currencies = []

    for item in data:
        currencies.append(CurrencyRate(
            currency_a=str(item["currencyCodeA"]),
            currency_b=str(item["currencyCodeB"]),
            date=timezone.make_aware(datetime.datetime.fromtimestamp(item["date"])),
            rate_buy=item.get("rateBuy", item.get("rateCross")),
            rate_sell=item.get("rateSell", item.get("rateCross")),
        ))

    CurrencyRate.objects.bulk_create(currencies, ignore_conflicts=True)
