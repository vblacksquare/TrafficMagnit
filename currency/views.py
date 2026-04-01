from django.db.models import Max, Q
from django.http import Http404
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view

from .models import CurrencyRate, TrackedCurrency, CurrencyChoices
from .serializers import CurrencyRateSerializer, TrackedCurrencySerializer


@extend_schema_view(
    get=extend_schema(operation_id="list_rates_latest")
)
class CurrencyRateListView(generics.ListAPIView):
    serializer_class = CurrencyRateSerializer

    def get_queryset(self):
        qs = CurrencyRate.objects.filter(currency_b=CurrencyChoices.UAH)

        latest_per_currency = qs.values('currency_a').annotate(latest_date=Max('date'))

        q_filter = Q()
        for item in latest_per_currency:
            q_filter |= Q(currency_a=item['currency_a'], date=item['latest_date'])

        return qs.filter(q_filter).order_by('currency_a')


@extend_schema(
    methods=['GET'],
    request=None,
    responses={
        200: OpenApiResponse(
            response={
                "type": "array",
                "items": {
                    "type": "string",
                    "example": "USD"
                }
            },
        )
    }
)
@api_view(['GET'])
def available_currencies(request):
    tracked = TrackedCurrency.objects.values_list('code', flat=True)

    available = [
        c.label
        for c in CurrencyChoices
        if c.value not in tracked
    ]

    return Response(available)


@extend_schema(
    methods=['POST'],
    request=TrackedCurrencySerializer,
    responses={
        200: TrackedCurrencySerializer,
        400: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Currency already tracked"}
                }
            }
        ),
        404: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Currency not found"}
                }
            }
        )
    }
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def add_currency(request):
    raw_code = request.data.get("code")
    code = CurrencyChoices.to_code(raw_code)
    if code is None:
        return Response({"error": "Currency not found"}, status=404)

    obj, created = TrackedCurrency.objects.get_or_create(code=code, user=request.user)
    if not created:
        return Response({"error": "Currency already tracked"}, status=400)

    serializer = TrackedCurrencySerializer(obj)
    return Response(serializer.data)


@extend_schema_view(
    get=extend_schema(operation_id="get_rates_history")
)
class CurrencyRateHistoryView(generics.ListAPIView):
    serializer_class = CurrencyRateSerializer
    BASE_CURRENCY_CODE = "980"

    def get_queryset(self):
        raw_code: str = self.kwargs.get('code')
        code = CurrencyChoices.to_code(raw_code)
        if code is None:
            return Response({"error": "Currency not found"}, status=404)

        params = self.request.query_params

        filters = {
            'currency_a': code,
            'currency_b': self.BASE_CURRENCY_CODE
        }

        if start := params.get('start'):
            filters['date__gte'] = start

        if end := params.get('end'):
            filters['date__lte'] = end

        return CurrencyRate.objects.filter(**filters).order_by('-date')


@extend_schema(
    methods=['POST'],
    request=None,
    responses={
        200: TrackedCurrencySerializer,
        400: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Currency tracking not created"}
                }
            }
        ),
        404: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Currency not found"}
                }
            }
        )
    }
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def toggle_currency(request, code):
    raw_code = code.upper()
    code = CurrencyChoices.to_code(raw_code)
    if code is None:
        return Response({"error": "Currency not found"}, status=404)

    try:
        currency = TrackedCurrency.objects.get(code=code, user=request.user)
        currency.is_active = not currency.is_active
        currency.save()
        return Response({"status": "ok", "is_active": currency.is_active})

    except TrackedCurrency.DoesNotExist:
        return Response({"error": "Currency tracking not created"}, status=400)
