from django.contrib import auth, messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, reverse

from .forms import LoginForm, RegisterForm, UserCompanyForm, EntryInvoiceForm, ExitInvoiceForm, PartnerForm
from .models import YourCompany, Partners, EntryInvoice, ExitInvoice


AuthUser = auth.get_user_model()


def home_view(request):
    return render(request, "home.html")


def emite_view(request):
    return render(request, "emite.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect(reverse("home"))

    return render(request, "register.html", {"form": RegisterForm})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect(reverse("home"))
        else:
            messages.error(request, "Adresa de email sau parola sunt gresite!")

    return render(request, "login.html", {"form": LoginForm})


def logout_view(request):
    auth.logout(request)
    messages.info(request, "Va-ti deconectat cu succes.")
    return redirect(reverse("home"))


def user_company_view(request):
    your_company = YourCompany.objects.filter(user=request.user)
    if request.method == "GET":
        if your_company:
            return render(request, "user_company.html", {"your_company": your_company})
        else:
            return render(request, "user_company.html", {"form": UserCompanyForm})
    elif request.method == "POST":
        form = UserCompanyForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("user_company"))


def user_company_edit_view(request):
    your_company = YourCompany.objects.get(user=request.user)
    form = UserCompanyForm(request.POST or None, instance=your_company)
    if form.is_valid():
        form.save()

        return redirect(reverse("user_company"))

    return render(request, 'user_company_edit.html', {"form": form})


def user_company_delete_view(request):
    your_company = YourCompany.objects.get(user=request.user)
    your_company.delete()

    return redirect(reverse("home"))


def entry_invoice_view(request):
    form = EntryInvoiceForm()
    form_2 = PartnerForm()
    your_company = YourCompany.objects.filter(user=request.user)
    context = {
        "form": form,
        "form_2": form_2,
        "your_company": your_company
    }
    if request.method == "POST":
        customer = YourCompany.objects.get(user=request.user)
        form = EntryInvoiceForm(request.POST, customer=customer)
        form_2 = PartnerForm(request.POST)

        if all([form.is_valid(), form_2.is_valid()]):

            form_2.save(commit=False)
            obj, created = Partners.objects.get_or_create(**form_2.cleaned_data)
            partner = Partners.objects.get(id=obj.pk)
            partner.user.add(request.user)
            child = form.save(commit=False)
            child.supplier = obj
            child.save()

            return redirect(reverse("home"))

    return render(request, "entry_invoice.html", context)


def exit_invoice_view(request):
    form = ExitInvoiceForm()
    form_2 = PartnerForm()
    your_company = YourCompany.objects.filter(user=request.user)
    context = {
        "form": form,
        "form_2": form_2,
        "your_company": your_company
    }
    if request.method == "POST":
        supplier = YourCompany.objects.get(user=request.user)
        form = ExitInvoiceForm(request.POST, supplier=supplier)
        form_2 = PartnerForm(request.POST)

        if all([form.is_valid(), form_2.is_valid()]):

            form_2.save(commit=False)
            obj, created = Partners.objects.get_or_create(**form_2.cleaned_data)
            partner = Partners.objects.get(id=obj.pk)
            partner.user.add(request.user)
            child = form.save(commit=False)
            child.customer = obj
            child.save()

            return redirect(reverse("home"))

    return render(request, "exit_invoice.html", context)


def entry_invoice_list_view(request):
    try:
        customer = YourCompany.objects.get(user=request.user)
        invoices = EntryInvoice.objects.filter(customer=customer)
    except ObjectDoesNotExist:
        return render(request, "entry_invoice_list.html")

    if invoices:
        return render(request, "entry_invoice_list.html", {"invoices": invoices})
    else:
        return render(request, "entry_invoice_list.html")


def entry_invoice_edit_view(request, invoice_id):
    your_company = YourCompany.objects.filter(user=request.user)
    invoice = EntryInvoice.objects.get(pk=invoice_id)
    partner = invoice.supplier
    form = EntryInvoiceForm(request.POST or None, instance=invoice)
    form_2 = PartnerForm(request.POST or None, instance=partner)
    context = {
        "form": form,
        "form_2": form_2,
        "your_company": your_company
    }
    if all([form.is_valid(), form_2.is_valid()]):
        form_2.save(commit=False)
        obj, created = Partners.objects.get_or_create(**form_2.cleaned_data)
        partner = Partners.objects.get(id=obj.pk)
        partner.user.add(request.user)
        child = form.save(commit=False)
        child.customer = obj
        child.save()

        return redirect(reverse("entry_invoice_list"))

    return render(request, "entry_invoice_edit.html", context)


def entry_invoice_delete_view(request, invoice_id):
    invoice = EntryInvoice.objects.get(pk=invoice_id)
    invoice.delete()

    return redirect(reverse("entry_invoice_list"))


def partner_list_view(request):
    partners = Partners.objects.filter(user=request.user)
    if partners:
        return render(request, "partner_list.html", {"partners": partners})
    else:
        return render(request, "partner_list.html")


def partner_edit_view(request, partner_id):
    partner = Partners.objects.get(pk=partner_id)
    form = PartnerForm(request.POST or None, instance=partner)
    if form.is_valid():
        form.save()
        return redirect(reverse("partners"))

    return render(request, "partner_edit.html", {"form": form})


def partner_delete_view(request, partner_id):
    partner = Partners.objects.get(pk=partner_id)
    partner.delete()

    return redirect(reverse("partners"))


def partner_add_view(request):
    form = PartnerForm()
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            obj = form.save()
            partner = Partners.objects.get(id=obj.pk)
            partner.user.add(request.user)

            return redirect(reverse("partners"))

    return render(request, "partner_add.html", {"form": form})
