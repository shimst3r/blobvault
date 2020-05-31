from django.conf import settings
from django.core import mail


def send_email(email, url):
    email_body = _generate_email_message(url=url)
    mail.send_mail(
        subject="Your Blob Vault Secret URL",
        message=email_body,
        from_email=settings.EMAIL_SENDER,
        recipient_list=[email],
        fail_silently=False,
    )


def _generate_email_message(url):  # pragma: no cover
    text = (
        "Dear stranger,\n\n"
        "Someone wants to share a secret with you! At the moment, it is securely"
        f" stored at {url} . To decrypt it, you will receive a secret key"
        " via a different channel.\n\nYou can download the content only once, it will"
        " be deleted afterwards. To download the decrypted secret, open the above URL"
        " and enter the secret key.\n\n"
        "Stay safe,\n"
        "Your Blob Vault Team"
    )

    return text
