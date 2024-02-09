from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .views import send_email_view


AuthUserModel = get_user_model()


@receiver(post_save, sender=AuthUserModel)
def send_new_account_email(instance, created, **kwargs):
    if created:
        send_email_view(instance)
