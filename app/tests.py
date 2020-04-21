import uuid

from django.conf import settings
from django.utils import timezone
from hypothesis import given
from hypothesis.strategies import binary, datetimes, integers
from hypothesis.extra.django import TestCase
from model_bakery import baker

from .models import Blob, Receipt


class BlobTestCase(TestCase):
    def test_blob_primary_key_is_uuid(self):
        blob = baker.make(Blob)
        self.assertIsInstance(blob.pk, uuid.UUID)

    @given(binary())
    def test_decrypt_encrypted_content(self, content):
        blob, key = Blob.encrypt_content(
            content=content, mimetype="application/octet-stream"
        )

        decrypted_content = blob.decrypt_content(fernet_key=key)

        self.assertEqual(content, decrypted_content)


class ReceiptTestCase(TestCase):
    def test_receipt_primary_key_is_uuid(self):
        receipt = baker.make(Receipt)
        self.assertIsInstance(receipt.pk, uuid.UUID)

    @given(datetimes(), integers(min_value=1, max_value=1000))
    def test_is_quota_reached(self, datetime, quantity):
        datetime = timezone.make_aware(datetime)
        baker.make(Receipt, creation_date=datetime, _quantity=quantity)

        expected = quantity >= int(settings.EMAIL_QUOTA)
        actual = Receipt.is_quota_reached(date=datetime.date())

        self.assertEqual(expected, actual)


# TODO: Add tests for download and upload views.
