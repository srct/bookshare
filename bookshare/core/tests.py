from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from .models import Student
from .views import DetailStudent, StudentRatings

class ProfileTest(TestCase):

    def test_username_resolves_to_profile(self):
        found = resolve('/student/username/')
        self.assertEqual(found.func, home_page)

        request = HttpResponse()
        reponse = profile(request)

        self.assertTrue(response.content.startswith('<html>'))
        self.assertIn('<title>user.get_full_name</title>', response.content)
        self.assertTrue(response.content.endswith('</html>'))

