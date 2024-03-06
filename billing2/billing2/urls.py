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
from django.urls import include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from billing_app.views import home_view
from billing_app.views import login_view
from billing_app.views import logout_view
from billing_app.views import register_view
from billing_app.views import user_company_view
from billing_app.views import user_company_edit_view
from billing_app.views import user_company_delete_view
from billing_app.views import entry_invoice_view
from billing_app.views import exit_invoice_view
from billing_app.views import partner_list_view
from billing_app.views import partner_edit_view
from billing_app.views import partner_delete_view
from billing_app.views import partner_add_view
from billing_app.views import entry_invoice_list_view
from billing_app.views import entry_invoice_edit_view
from billing_app.views import entry_invoice_delete_view
from billing_app.views import exit_invoice_list_view
from billing_app.views import exit_invoice_edit_view
from billing_app.views import exit_invoice_delete_view
from billing_app.views import YourCompanyViewSet


router = routers.DefaultRouter()
router.register(r'user-companies', YourCompanyViewSet, 'user-companies')

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', home_view, name="home"),
    path('inregistrare/', register_view, name='register'),
    path('autentificare/', login_view, name='login'),
    path('deconectare/', logout_view, name='logout'),
    path('firma-ta/', user_company_view, name='user_company'),
    path('firma-ta/editare/', user_company_edit_view, name='user_company_edit'),
    path('firma-ta/stergere/', user_company_delete_view, name='user_company_delete'),
    path('emitere/intrare/', entry_invoice_view, name='entry_invoice'),
    path('lista-parteneri/', partner_list_view, name='partners'),
    path('partener-modificare/<partner_id>', partner_edit_view, name='partner_edit'),
    path('sterge-partener/<partner_id>', partner_delete_view, name='partner_delete'),
    path('adauga-partener/', partner_add_view, name='partner_add'),
    path('emitere/iesire/', exit_invoice_view, name='exit_invoice'),
    path('facturi/intrare/', entry_invoice_list_view, name='entry_invoice_list'),
    path('facturi/intrare-modificare/<invoice_id>', entry_invoice_edit_view, name='entry_invoice_edit'),
    path('facturi/intrare-stergere/<invoice_id>', entry_invoice_delete_view, name='entry_invoice_delete'),
    path('facturi/iesire/', exit_invoice_list_view, name='exit_invoice_list'),
    path('facturi/iesire-modificare/<invoice_id>', exit_invoice_edit_view, name='exit_invoice_edit'),
    path('facturi/iesire-stergere/<invoice_id>', exit_invoice_delete_view, name='exit_invoice_delete'),
    path('api/', include(router.urls)),
    path('api/auth/', jwt_views.TokenObtainPairView.as_view(), name='api-auth'),
    path('api/auth/refresh', jwt_views.TokenRefreshView.as_view(), name='api-auth-refresh'),

]

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
