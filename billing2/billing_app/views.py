from django.contrib import auth, messages
from django.shortcuts import redirect, render, reverse

from .forms import LoginForm, RegisterForm, UserCompanyForm, EntryInvoiceForm, PartnerForm
from .models import YourCompany, PartnerUser, Partners


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
    if request.method == "POST":
        customer = YourCompany.objects.get(user=request.user)
        form = EntryInvoiceForm(request.POST, customer=customer)
        if form.is_valid():
            form.save()
            return redirect(reverse("home"))

    return render(request, "entry_invoice.html", {"form": EntryInvoiceForm})
    # SAVE METHOD FOR PARTNERS WITH M2M FIELD !!!
    # if request.method == "POST":
    #     form = PartnerForm(request.POST)
    #     if form.is_valid():
    #         obj, created = form.save() or Partners.objects.get_or_create(**form.cleaned_data)...https://stackoverflow.com/questions/2297820/django-forms-with-get-or-create
    #         partner = Partners.objects.get(id=obj.pk)
    #          MAYBE A TRY AND EXCEPT HERE FOR THE EXISTING M2M RELATIONSHIPS!!!!
    #         partner.user.add(request.user)
    #         return redirect(reverse("home"))
    #
    # return render(request, "entry_invoice.html", {"form": PartnerForm})
