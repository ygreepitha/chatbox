from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Document
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class ChatAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        # Clean up any documents created during tests
        Document.objects.all().delete()
        if os.path.exists('test.pdf'):
            os.remove('test.pdf')

    def test_upload_document(self):
        # Simulate a file upload
        file = SimpleUploadedFile("test.pdf", b"Dummy content", content_type="application/pdf")
        response = self.client.post(reverse('document-upload'), {'file': file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 1)

    def test_query_response(self):
        # Upload a sample PDF document first
        file = SimpleUploadedFile("test.pdf", b"Dummy content", content_type="application/pdf")
        self.client.post(reverse('document-upload'), {'file': file})

        # Test querying the document
        query = {"query": "What is the document about?"}
        response = self.client.post(reverse('chat_api'), query, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("answer", response.data)

