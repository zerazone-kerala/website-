from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from .models import Project, DownloadRecord
from .admin import DownloadRecordAdmin, export_as_csv
import csv
import io

class MockRequest:
    pass

class AdminCSVTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(title="Test Project", description="Test Description")
        self.record = DownloadRecord.objects.create(
            project=self.project,
            name="John Doe",
            email="john@example.com",
            phone="1234567890"
        )
        self.site = AdminSite()

    def test_export_as_csv(self):
        # Create a queryset
        queryset = DownloadRecord.objects.all()
        
        # Call the action
        modeladmin = DownloadRecordAdmin(DownloadRecord, self.site)
        request = MockRequest()
        response = export_as_csv(modeladmin, request, queryset)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        
        # Check content
        content = response.content.decode('utf-8')
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        
        # Header + 1 row
        self.assertEqual(len(rows), 2)
        
        # Verify header (implementation specific, but should contain fields)
        self.assertIn('name', rows[0])
        self.assertIn('email', rows[0])
        
        # Verify data
        self.assertIn('John Doe', rows[1])
        self.assertIn('john@example.com', rows[1])

