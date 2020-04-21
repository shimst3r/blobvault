import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from hypothesis import example, given
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

    @given(datetime=datetimes(), quantity=integers(min_value=1, max_value=200))
    @example(datetime=datetime.now(), quantity=settings.EMAIL_QUOTA)
    def test_is_quota_reached(self, datetime, quantity):
        datetime = timezone.make_aware(datetime)
        baker.make(Receipt, creation_date=datetime, _quantity=quantity)

        expected = quantity >= settings.EMAIL_QUOTA
        actual = Receipt.is_quota_reached(date=datetime.date())

        self.assertEqual(expected, actual)

    @given(datetimes(), integers(min_value=1, max_value=10))
    def test_daily_amount(self, datetime, quantity):
        datetime = timezone.make_aware(datetime)
        day_before = datetime - timedelta(days=1)
        day_after = datetime + timedelta(days=1)

        baker.make(Receipt, creation_date=day_before, _quantity=quantity)
        baker.make(Receipt, creation_date=datetime, _quantity=quantity)
        baker.make(Receipt, creation_date=day_after, _quantity=quantity)

        expected_amount = quantity
        actual_amount = Receipt._daily_amount(date=datetime.date())

        self.assertEqual(expected_amount, actual_amount)
