from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_email_view(user):
    context = {
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    template = get_template("email/email_template.html")
    content = template.render(context)

    mail = EmailMultiAlternatives(
        subject="New account created.",
        body=content,
        to=[user.email],
    )

    mail.content_subtype = "html"
    mail.send()
