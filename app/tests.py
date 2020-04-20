import uuid

from hypothesis import given
from hypothesis.strategies import binary, datetimes
from hypothesis.extra.django import TestCase
from model_bakery import baker

from .models import Blob, Receipt


class BlobTestCase(TestCase):
    def setUp(self):
        self.blob = baker.make(Blob)

    def test_blob_primary_key_is_uuid(self):
        self.assertIsInstance(self.blob.pk, uuid.UUID)

    @given(binary())
    def test_decrypt_encrypted_content(self, content):
        blob, key = Blob.encrypt_content(
            content=content, mimetype="application/octet-stream"
        )

        decrypted_content = blob.decrypt_content(fernet_key=key)

        self.assertEqual(content, decrypted_content)


class ReceiptTestCase(TestCase):
    def setUp(self):
        self.receipt = baker.make(Receipt)

    def test_receipt_primary_key_is_uuid(self):
        self.assertIsInstance(self.receipt.pk, uuid.UUID)

    @given(datetimes())
    def test_daily_amounts_of_receipts(self, datetime):
        baker.make(Receipt, creation_date=datetime)

        expected_daily_amount = 1
        actual_daily_amount = Receipt.daily_amount(date=datetime.date())

        self.assertEqual(expected_daily_amount, actual_daily_amount)


# TODO: Add tests for download and upload views.
