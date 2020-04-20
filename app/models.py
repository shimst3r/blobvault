import base64
import uuid

from cryptography import fernet
from django.db import models


class Blob(models.Model):
    content = models.BinaryField()
    creation_date = models.DateTimeField(auto_now_add=True)
    mimetype = models.TextField()
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)

    @classmethod
    def encrypt_content(cls, content, mimetype):
        encoded_content = base64.b64encode(content)

        key = fernet.Fernet.generate_key()
        cipher_suite = fernet.Fernet(key)
        encrypted_content = cipher_suite.encrypt(encoded_content)

        blob = cls(content=encrypted_content, mimetype=mimetype)

        return blob, key

    def decrypt_content(self, fernet_key):
        cipher_suite = fernet.Fernet(fernet_key)
        decrypted_content = cipher_suite.decrypt(self.content)
        decoded_content = base64.b64decode(decrypted_content)

        return decoded_content


class Receipt(models.Model):
    creation_date = models.DateTimeField()
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)

    @classmethod
    def daily_amount(cls, date):
        """
        Returns the number of receipts that have been issued on a given date.
        """
        return cls.objects.filter(creation_date__date=date).count()
