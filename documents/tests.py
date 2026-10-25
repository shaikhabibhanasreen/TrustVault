from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Document, DocumentPermission

User = get_user_model()


class DocumentSearchTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner_test",
            password="TestPass123!"
        )

        self.viewer = User.objects.create_user(
            username="viewer_test",
            password="TestPass123!"
        )

        self.private_document = Document.objects.create(
            title="Private Report",
            description="Confidential report",
            category="Reports",
            file=SimpleUploadedFile(
                "private.txt",
                b"Private test file",
                content_type="text/plain"
            ),
            owner=self.owner,
        )

        self.shared_document = Document.objects.create(
            title="Vegetables Report",
            description="Fresh vegetables inventory",
            category="Education",
            file=SimpleUploadedFile(
                "vegetables.txt",
                b"Vegetables test file",
                content_type="text/plain"
            ),
            owner=self.owner,
        )

        DocumentPermission.objects.create(
            document=self.shared_document,
            user=self.viewer,
            permission_type=DocumentPermission.VIEW,
            granted_by=self.owner,
        )

    def test_owner_can_see_owned_documents(self):
        self.client.login(
            username="owner_test",
            password="TestPass123!"
        )

        response = self.client.get(reverse("document_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Private Report")
        self.assertContains(response, "Vegetables Report")

    def test_viewer_can_see_shared_document(self):
        self.client.login(
            username="viewer_test",
            password="TestPass123!"
        )

        response = self.client.get(reverse("document_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vegetables Report")
        self.assertNotContains(response, "Private Report")

    def test_search_by_category(self):
        self.client.login(
            username="viewer_test",
            password="TestPass123!"
        )

        response = self.client.get(
            reverse("document_list"),
            {"q": "Education"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vegetables Report")
        self.assertNotContains(response, "Private Report")

    def test_search_with_no_results(self):
        self.client.login(
            username="viewer_test",
            password="TestPass123!"
        )

        response = self.client.get(
            reverse("document_list"),
            {"q": "xyz123notfound"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No documents found")