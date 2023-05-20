from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from accounts.validators import valid_password
from django.db.models import Q
from accounts.exceptions import RegisterationEmailOrPhoneExists, PhoneOrPasswordWrong
from accounts.utils import get_token_pair
from redis_driver.core import redis_client



class PhoneNumberSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region="IR")
    
    def is_active_user(self):
        phone_number = self.validated_data.get("phone_number")
        User = get_user_model()
        if User.objects.filter(phone_number=phone_number, is_active=True).exists():
            return True
        return False



class OtpSerializer(PhoneNumberSerializer):
    otp_number = serializers.IntegerField(max_value=999999, min_value=100000)

    def otp_exists(self)->bool:
        phone_number = self.validated_data.get("phone_number")
        otp_number = self.validated_data.get("otp_number")
        cached_otp = redis_client.get("otp:phone_number:" + str(phone_number))
        
        if cached_otp is not None:
            if int(cached_otp) == otp_number:
                return True
        return False


class RegisterSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=False)
    first_name = serializers.CharField(max_length=127, min_length=5)
    last_name = serializers.CharField(max_length=127, min_length=5)
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_password2(self, password2):
        password1 = self.initial_data.get("password1")
        valid_password(
            password1=password1,
            password2=password2
        )
        return password2


    def create(self, validated_data):
        User = get_user_model()
        password = validated_data.get("password")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        email = validated_data.get("email")
        phone_number = self.context.get("request").user.get("phone_number")
        if User.objects.filter(Q(email=email) | Q(phone_number=phone_number)).exists():
            raise RegisterationEmailOrPhoneExists({
                "error": "Email Exists!"
            })
        user = User(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save()
        return user



class TokenPairSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region="IR")
    password = serializers.CharField()

    def validate_password(self, password):
        valid_password(
            password1=password,
            password2=password
        )
        return password
    
    def get_token(self):
        phone_number = self.validated_data.get("phone_number")
        password = self.validated_data.get("password")
        user = self.get_user(phone_number, password)
        token_pair = get_token_pair(user)
        return token_pair

    def get_user(self, pn, password):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(
                phone_number = pn
            )
        except:
            raise PhoneOrPasswordWrong({"error": "Phone or password wrong."})
        if not user.check_password(password):
            raise PhoneOrPasswordWrong({"error": "Phone or password wrong."})
        return user

