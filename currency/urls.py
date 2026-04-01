from django.urls import path
from .views import (
    CurrencyRateListView,
    CurrencyRateHistoryView,
    available_currencies,
    add_currency,
    toggle_currency,
)


urlpatterns = [
    path('rates/', CurrencyRateListView.as_view(), name='rates-list'),
    path('rates/<str:code>/', CurrencyRateHistoryView.as_view(), name='rates-history'),
    path('currencies/available/', available_currencies, name='available-currencies'),
    path('currencies/add/', add_currency, name='add-currency'),
    path('currencies/<str:code>/toggle/', toggle_currency, name='toggle-currency'),
]
