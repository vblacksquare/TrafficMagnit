
from rest_framework import serializers
from .models import CurrencyRate, TrackedCurrency


class CurrencyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = ['id', 'currency_a', 'currency_b', 'date', 'rate_buy', 'rate_sell']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['currency_a'] = instance.get_currency_a_display()
        data['currency_b'] = instance.get_currency_b_display()

        return data

class TrackedCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackedCurrency
        fields = ['id', 'code', 'is_active']
