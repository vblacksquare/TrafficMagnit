
from django.conf import settings
from django.db import models
from rest_framework.response import Response


class CurrencyChoices(models.TextChoices):
    UAH = "980", "UAH"
    USD = "840", "USD"
    EUR = "978", "EUR"
    GBP = "826", "GBP"
    JPY = "392", "JPY"
    CHF = "756", "CHF"
    CNY = "156", "CNY"
    RUB = "643", "RUB"

    AED = "784", "AED"
    AFN = "971", "AFN"
    ALL = "8", "ALL"
    AMD = "51", "AMD"
    AOA = "973", "AOA"
    ARS = "32", "ARS"
    AUD = "36", "AUD"
    AZN = "944", "AZN"
    BDT = "50", "BDT"
    BGN = "975", "BGN"
    BHD = "48", "BHD"
    BIF = "108", "BIF"
    BND = "96", "BND"
    BOB = "68", "BOB"
    BRL = "986", "BRL"
    BWP = "72", "BWP"
    BYN = "933", "BYN"
    CAD = "124", "CAD"
    CDF = "976", "CDF"
    CLP = "152", "CLP"
    COP = "170", "COP"
    CRC = "188", "CRC"
    CUP = "192", "CUP"
    CZK = "203", "CZK"
    DJF = "262", "DJF"
    DKK = "208", "DKK"
    DOP = "214", "DOP"
    DZD = "12", "DZD"
    EGP = "818", "EGP"
    ETB = "230", "ETB"
    GEL = "981", "GEL"
    GHS = "936", "GHS"
    GMD = "270", "GMD"
    GNF = "324", "GNF"
    HKD = "344", "HKD"
    HRK = "191", "HRK"
    HUF = "348", "HUF"
    IDR = "360", "IDR"
    ILS = "376", "ILS"
    INR = "356", "INR"
    IQD = "368", "IQD"
    IRR = "364", "IRR"
    ISK = "352", "ISK"
    JOD = "400", "JOD"
    KES = "404", "KES"
    KGS = "417", "KGS"
    KHR = "116", "KHR"
    KPW = "408", "KPW"
    KRW = "410", "KRW"
    KWD = "414", "KWD"
    KZT = "398", "KZT"
    LAK = "418", "LAK"
    LBP = "422", "LBP"
    LKR = "144", "LKR"
    LYD = "434", "LYD"
    MAD = "504", "MAD"
    MDL = "498", "MDL"
    MGA = "969", "MGA"
    MKD = "807", "MKD"
    MNT = "496", "MNT"
    MRO = "478", "MRO"
    MUR = "480", "MUR"
    MVR = "462", "MVR"
    MWK = "454", "MWK"
    MXN = "484", "MXN"
    MYR = "458", "MYR"
    MZN = "943", "MZN"
    NAD = "516", "NAD"
    NGN = "566", "NGN"
    NIO = "558", "NIO"
    NOK = "578", "NOK"
    NPR = "524", "NPR"
    NZD = "554", "NZD"
    OMR = "512", "OMR"
    PEN = "604", "PEN"
    PHP = "608", "PHP"
    PKR = "586", "PKR"
    PLN = "985", "PLN"
    PYG = "600", "PYG"
    QAR = "634", "QAR"
    RON = "946", "RON"
    RSD = "941", "RSD"
    SAR = "682", "SAR"
    SCR = "690", "SCR"
    SDG = "938", "SDG"
    SEK = "752", "SEK"
    SGD = "702", "SGD"
    SLL = "694", "SLL"
    SOS = "706", "SOS"
    SRD = "968", "SRD"
    SYP = "760", "SYP"
    SZL = "748", "SZL"
    THB = "764", "THB"
    TJS = "972", "TJS"
    TMT = "795", "TMT"
    TND = "788", "TND"
    TRY = "949", "TRY"
    TWD = "901", "TWD"
    TZS = "834", "TZS"
    UGX = "800", "UGX"
    UYU = "858", "UYU"
    UZS = "860", "UZS"
    VEF = "937", "VEF"
    VND = "704", "VND"
    XAF = "950", "XAF"
    XDR = "960", "XDR"
    XOF = "952", "XOF"
    YER = "886", "YER"
    ZAR = "710", "ZAR"
    ZMK = "894", "ZMK"

    XAU = "959", "XAU"
    XAG = "961", "XAG"
    XPT = "962", "XPT"
    XPD = "964", "XPD"

    @classmethod
    def to_code(cls, value_or_name):
        if value_or_name in cls.values:
            return value_or_name

        try:
            return getattr(cls, str(value_or_name).upper())
        except (AttributeError, TypeError):
            return None


class CurrencyRate(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['currency_a', 'currency_b', 'date'],
                name='unique_currency_date'
            )
        ]
        ordering = ['currency_a', 'currency_b', '-date']

    currency_a = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices
    )
    currency_b = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices
    )
    date = models.DateTimeField()
    rate_buy = models.DecimalField(max_digits=12, decimal_places=4)
    rate_sell = models.DecimalField(max_digits=12, decimal_places=4)


class TrackedCurrency(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tracked_currencies"
    )
    code = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        unique=True
    )
    is_active = models.BooleanField(default=True)
