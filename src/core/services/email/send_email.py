from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from core.models import Token
from core.tasks import send_email


def send_template_email(subject, html_message, recipient_list):
    send_email.delay(subject=subject, html_message=html_message, recipient_list=recipient_list)


def send_email_verification(user, token: Token):
    # TODO Improvements
    title = _("Verify your email address.")
    text = _("Finish your registration with verifying your email.\nClick at link below to complete registration.")
    organization = "Q&A service."
    button_link = ""  # TODO button link
    button_text = _("Confirm.")
    html_message = render_to_string(
        "email/base.html",
        context={
            "title": title,
            "text": text,
            "organization": organization,
            "button_link": button_link,
            "button_text": button_text,
            "token": token.value,
        },
    )
    send_template_email(_("Email Verification"), html_message, [user.email])


def send_reset_password_email(user, token: Token):
    # TODO Improvements
    title = _("Reset password.")
    text = _("To reset password click at link below.")
    organization = "Q&A service."
    button_link = ""  # TODO button link
    button_text = _("Reset.")
    html_message = render_to_string(
        "email/base.html",
        context={
            "title": title,
            "text": text,
            "organization": organization,
            "button_link": button_link,
            "button_text": button_text,
            "token": token.value,
        },
    )
    send_template_email(_("Reset password"), html_message, [user.email])
