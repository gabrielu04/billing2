from django.db import models
from django.contrib.auth import get_user_model


AuthUser = get_user_model()


# Create your models here.
class Company(models.Model):
    class Meta:
        abstract = True

    nume = models.CharField(max_length=255)
    cod_fiscal = models.CharField(max_length=10)
    cod_onrc = models.CharField(max_length=255)


class YourCompany(Company):
    class Meta:
        db_table = "your_company"

    class VatType(models.TextChoices):
        PLATITOR = "Platitor", "Platitor"
        NEPLATITOR = "Neplatitor", "Neplatitor"

    nume = models.CharField(max_length=255, unique=True)
    cod_fiscal = models.CharField(max_length=10, unique=True)
    cod_onrc = models.CharField(max_length=255, unique=True)
    judet = models.CharField(max_length=255)
    localitate = models.CharField(max_length=255)
    street = models.CharField(max_length=255, null=True)
    street_no = models.CharField(max_length=20, null=True)
    tva = models.CharField(max_length=max(len(VatType.PLATITOR), len(VatType.NEPLATITOR)),
                           choices=VatType.choices)
    address_other_info = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)


class Partners(Company):
    class Meta:
        db_table = "partner"
    adresa = models.CharField(max_length=300)
    user = models.ManyToManyField(AuthUser, through="PartnerUser", related_name="PartnersUsers")


class PartnerUser(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE)


class Invoice(models.Model):
    class Meta:
        abstract = True

    # class VatRate(models.TextChoices):
    #     COTA_STANDARD = 0.19, 19
    #     COTA_9 = 0.09, 9
    #     COTA_5 = 0.05, 5
    #     COTA_0 = 0, 0

    series = models.CharField(max_length=5)
    number = models.IntegerField(unique=True)
    date = models.DateField()
    product_name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    price_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    vat_rate = models.FloatField(choices=((0.19, 19), (0.09, 9), (0.05, 5), (0, 0)))
    vat_ammount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    total_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    # # CALCULAREA SUMELOR AR PUTEA FI FACUTA DIN TEMPLATE SI PASATA IN DB APOI


class EntryInvoice(Invoice):
    class Meta:
        db_table = "entry_invoice"

    customer = models.ForeignKey(YourCompany, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Partners, on_delete=models.CASCADE)


class ExitInvoice(Invoice):
    class Meta:
        db_table = "exit_invoice"

    customer = models.ForeignKey(Partners, on_delete=models.CASCADE)
    supplier = models.ForeignKey(YourCompany, on_delete=models.CASCADE)
