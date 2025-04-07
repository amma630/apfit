from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTestCase(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")
        self.assertEqual(user.username, "testuser")
