from django.test import TestCase
from accounts.serializers.phone import PhoneNumberSerializer
from django.contrib.auth import get_user_model


class TestPhoneNumberSerializer(TestCase):
    def setUp(self) -> None:
        self.serializer = PhoneNumberSerializer
        self.user_model = get_user_model()

        # right inputs for user
        self.user = self.user_model.objects.create_user(
            phone_number="09190503468",
            email="mooooo@mo.com",
            password="asdmklasmdlamsdlasd"
        )
    
    def test_wrong_phone_number(self):
        data = {"phone_number": "919505012"}
        serializer = self.serializer(
            data=data
        )
        self.assertEqual(serializer.is_valid(), False)

    def test_right_phone_number(self):
        data = {"phone_number": "9195050120"}
        serializer = self.serializer(
            data=data
        )
        self.assertEqual(serializer.is_valid(), True)

    def test_is_active_for_real_user(self):
        data = {"phone_number": str(self.user.phone_number)}
        serializer = self.serializer(
            data=data
        )
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(serializer.is_active_user(), True)

    def test_is_active_for_fake_user(self):
        data = {"phone_number": "9190503444"}
        serializer = self.serializer(
            data=data
        )
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(serializer.is_active_user(), False)