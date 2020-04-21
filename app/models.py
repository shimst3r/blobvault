import base64
import uuid

from cryptography import fernet
from django.conf import settings
from django.db import models


class Blob(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content: models.BinaryField = models.BinaryField()
    creation_date: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    mimetype: models.TextField = models.TextField()

    @classmethod
    def encrypt_content(cls, content, mimetype):
        encoded_content = base64.b64encode(content)

        key = fernet.Fernet.generate_key()
        cipher_suite = fernet.Fernet(key)
        encrypted_content = cipher_suite.encrypt(encoded_content)

        blob = cls(content=encrypted_content, mimetype=mimetype)

        return blob, key.decode("utf-8")

    def decrypt_content(self, fernet_key):
        try:
            cipher_suite = fernet.Fernet(fernet_key.encode())
            decrypted_content = cipher_suite.decrypt(self.content)
            decoded_content = base64.b64decode(decrypted_content)
        except Exception:
            # Use a catch-all `Exception` for easier error propagation. This is
            # a deliberate decision and not best practice!
            raise fernet.InvalidToken
        else:
            return decoded_content


class Receipt(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4)
    creation_date: models.DateTimeField = models.DateTimeField()

    @classmethod
    def is_quota_reached(cls, date):
        """
        Returns `True` if the number of Receipts created on a given day exceeds
        the daily email quota.

        This is useful for preventing surprise bills from SendGrid.
        """
        return cls._daily_amount(date=date) >= int(settings.EMAIL_QUOTA)

    @classmethod
    def _daily_amount(cls, date):
        """
        Returns the number of receipts that have been issued on a given date.
        """
        return cls.objects.filter(creation_date__date=date).count()
