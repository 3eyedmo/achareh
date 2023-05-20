from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

class TestUserModel(TestCase):
    def setUp(self) -> None:
        self.user_model = get_user_model()

        # right inputs for user
        self.user = self.user_model.objects.create_user(
            phone_number="+989190503479",
            email="mooooo@mo.com",
            password="asdmklasmdlamsdlasd"
        )

    def test_invalid_phone_number(self):
        # invalid phone_number for user
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user(
                phone_number="91905034",
                email="fake@mo.com",
                password="asdmklasmdlamsdlasd"
            )
    
    def test_duplicate_email(self):
        # duplicate email for user
        with self.assertRaises(IntegrityError):
            self.user_model.objects.create_user(
                phone_number="+989197584562",
                email="mooooo@mo.com",
                password="asdmklasmdlamsdlasd"
            )
    
    def test_duplicate_phonenumber(self):
        # duplicate phone number for user
        with self.assertRaises(IntegrityError):
            self.user_model.objects.create_user(
                phone_number="+989190503479",
                email="fake@mo.com",
                password="asdmklasmdlamsdlasd"
            )
