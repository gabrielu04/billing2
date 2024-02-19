"""
URL configuration for billing2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from billing_app.views import emite_view
from billing_app.views import home_view
from billing_app.views import login_view
from billing_app.views import logout_view
from billing_app.views import register_view
from billing_app.views import user_company_view
from billing_app.views import user_company_edit_view
from billing_app.views import user_company_delete_view
from billing_app.views import entry_invoice_view


urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', home_view, name="home"),
    path('emite-factura/', emite_view, name="emite"),
    path('inregistrare/', register_view, name="register"),
    path('autentificare/', login_view, name='login'),
    path('deconectare/', logout_view, name='logout'),
    path('firma-ta/', user_company_view, name='user_company'),
    path('firma-ta/editare/', user_company_edit_view, name='user_company_edit'),
    path('firma-ta/stergere/', user_company_delete_view, name='user_company_delete'),
    path('emitere/intrare/', entry_invoice_view, name='entry_invoice'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
