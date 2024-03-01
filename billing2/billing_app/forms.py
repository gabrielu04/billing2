from django import forms
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.html import format_html_join
from django.utils.translation import gettext_lazy as _

from .models import YourCompany, EntryInvoice, ExitInvoice, Partners

import calculation


AuthUserModel = get_user_model()


# Coppied function to help writting html of the help texts of password
def add_help_text(ar):
    help_texts = ar
    help_items = format_html_join(
        "", "<li>{}</li>", ((help_text,) for help_text in help_texts)
    )
    return format_html("<ul>{}</ul>", help_items) if help_items else ""


# Calling the html writting function to write the translated password help texts.
help_text_list = ["Parola nu trebuie sa fie similara cu alte informatii personale.",
                  "Parola trebuie sa contina minim 8 caractere.",
                  "Parola nu trebuie sa fie una utilizata frecvent.",
                  "Parola nu poate contine numai caractere numerice."]

password_help_texts = add_help_text(help_text_list)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = AuthUserModel
        fields = ["first_name", "last_name", "email"]
        labels = {
            "first_name": _("Prenume"),
            "last_name": _("Nume de familie"),
            "email": _("Adresa de email")
        }

    password = forms.CharField(label="Parola", widget=forms.PasswordInput,
                               required=True, help_text=password_help_texts)
    password_confirmation = forms.CharField(label="Confirmare parola", widget=forms.PasswordInput, required=True)

    def save(self, commit=True):
        password = self.cleaned_data["password"]
        self.instance.set_password(password)
        return super().save(commit)


class LoginForm(forms.Form):
    email = forms.EmailField(label="Adresa de email", required=True)
    password = forms.CharField(label="Parola", widget=forms.PasswordInput, required=True)
    remember_me = forms.BooleanField(label="Tine-ma minte", required=False)


class UserCompanyForm(forms.ModelForm):
    class Meta:
        model = YourCompany
        fields = ["nume", "tva", "cod_fiscal", "cod_onrc", "judet",
                  "localitate", "street", "street_no", "address_other_info"]
        labels = {
            "nume": _("Denumire"),
            "tva": _("Regim TVA"),
            "cod_fiscal": _("CUI"),
            "cod_onrc": _("Nr. Inregistrare"),
            "judet": _("Judet"),
            "localitate": _("Localitate"),
            "street": _("Strada"),
            "street_no": _("Nr."),
            "address_other_info": _("Alte informatii despre adresa"),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(UserCompanyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(UserCompanyForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance


# Date input class for date field in invoice to show the date widget in browser
class DateInputType(forms.DateInput):
    input_type = 'date'


# Forms for invoices
class EntryInvoiceForm(forms.ModelForm):
    class Media:
        js = ['vat_ammount.js']

    class Meta:
        model = EntryInvoice
        fields = ["series", "number", "date", "product_name", "price", "unit",
                  "quantity", "price_quantity", "vat_rate", "vat_ammount", "total_pay"]
        labels = {
            "series": _("Serie"),
            "number": _("Nr"),
            "date": _("Data"),
            "product_name": _("Produs/serviciu"),
            "quantity": _("Cantitate"),
            "unit": _("Unitate de masura"),
            "price": _("Pret unitar"),
            "price_quantity": _("Valoare"),
            "vat_rate": _("Cota TVA (%)"),
            "vat_ammount": _("TVA"),
            "total_pay": _("Total de plata")
        }
        widgets = {
            "date": DateInputType(),
            "price_quantity": calculation.FormulaInput('parseFloat(quantity*price).toFixed(2)', attrs={"class": "qp"}),
            "vat_rate": forms.Select(attrs={"class": "vatr"}),
            "vat_ammount": forms.NumberInput(attrs={"class": "vata"}),
            "total_pay": calculation.FormulaInput('parseFloat(price_quantity+vat_ammount).toFixed(2)')
        }


    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop("customer", None)
        super(EntryInvoiceForm, self).__init__(*args, **kwargs)


    def save(self, commit=True):
        instance = super(EntryInvoiceForm, self).save(commit=False)
        if self.customer:
            instance.customer = self.customer
        if commit:
            instance.save()
        return instance


class ExitInvoiceForm(forms.ModelForm):
    class Meta:
        model = ExitInvoice
        fields = ["series", "number", "date", "product_name", "price", "unit",
                  "quantity", "price_quantity", "vat_rate", "vat_ammount", "total_pay"]
        labels = {
            "series": _("Serie"),
            "number": _("Nr"),
            "date": _("Data"),
            "product_name": _("Produs/serviciu"),
            "quantity": _("Cantitate"),
            "unit": _("Unitate de masura"),
            "price": _("Pret unitar"),
            "price_quantity": _("Valoare"),
            "vat_rate": _("Cota TVA (%)"),
            "vat_ammount": _("TVA"),
            "total_pay": _("Total de plata")
        }
        widgets = {
            "date": DateInputType(),
            "price_quantity": calculation.FormulaInput('parseFloat(quantity*price).toFixed(2)', attrs={"class": "qp"}),
            "vat_rate": forms.Select(attrs={"class": "vatr"}),
            "vat_ammount": forms.NumberInput(attrs={"class": "vata"}),
            "total_pay": calculation.FormulaInput('parseFloat(price_quantity+vat_ammount).toFixed(2)')
        }


    def __init__(self, *args, **kwargs):
        self.supplier = kwargs.pop("supplier", None)
        super(ExitInvoiceForm, self).__init__(*args, **kwargs)


    def save(self, commit=True):
        instance = super(ExitInvoiceForm, self).save(commit=False)
        if self.supplier:
            instance.supplier = self.supplier
        if commit:
            instance.save()
        return instance


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partners
        fields = ["nume", "cod_fiscal", "cod_onrc", "adresa"]
        labels = {
            "nume": _("Nume"),
            "cod_fiscal": _("CUI"),
            "cod_onrc": _("Cod inregistrare"),
            "adresa": _("Adresa"),
        }
