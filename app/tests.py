import uuid

from hypothesis import given
from hypothesis.strategies import binary
from hypothesis.extra.django import TestCase
from model_bakery import baker

from .models import Blob


class BlobTestCase(TestCase):
    def setUp(self):
        self.blob = baker.make(Blob)

    def test_blob_primary_key_is_uuid(self):
        self.assertIsInstance(self.blob.pk, uuid.UUID)

    @given(binary())
    def test_decrypt_encrypted_content(self, content):
        blob, key = Blob.encrypt_content(content=content)

        decrypted_content = blob.decrypt_content(fernet_key=key)

        self.assertEqual(content, decrypted_content)


# TODO: Add tests for download and upload views.
