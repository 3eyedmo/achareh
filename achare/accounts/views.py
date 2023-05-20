from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from redis_driver.core import redis_client

from accounts.serializers.phone import (
    PhoneNumberSerializer, OtpSerializer, RegisterSerializer, TokenPairSerializer
)
from accounts.permissions import OTPAuthenticated
from accounts.tokens import get_token_for_phone_number
from accounts.utils import get_token_pair
from accounts.decorators import login_throttle
from accounts.core import cache
from accounts.core import utils


class PhoneNumberApiView(GenericAPIView):
    serializer_class=PhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_active_user():
            return Response(data={"message": "user exists"}, status=status.HTTP_200_OK)
        
        code = utils.get_code()
        redis_client.set("otp:phone_number:" + str(serializer.validated_data.get("phone_number")), code, 150)
        cache.otp_limit_for_ip(request)
        return Response(data={"message": "need to register", "oneTimeCode": code}, status=status.HTTP_200_OK)






class OTPPhoneNumberApiView(GenericAPIView):
    serializer_class=OtpSerializer

    def post(self, request, *args, **kwargs):
        cache.is_otp_ip_banned(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get("phone_number")
        cache.check_otp_pn_is_banned(phone_number)
        if serializer.otp_exists():
            cache.delete_banned_pn(phone_number)
            cache.delete_otp_ip(request)
            response = Response(data={
                "message": "valid otp",
                "token": get_token_for_phone_number(str(phone_number))
            }, status=status.HTTP_200_OK)
            return response
        cache.otp_pn_limiter(phone_number=phone_number)
        cache.ban_ip_for_otp(request)
        return Response({"message": "wrong otp number"}, status=status.HTTP_404_NOT_FOUND)



class RegisterApiView(GenericAPIView):
    serializer_class=RegisterSerializer
    permission_classes=(OTPAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        return Response(data={"message": "ok", "tokens": get_token_pair(user)})



class TokenPairApiView(GenericAPIView):
    serializer_class=TokenPairSerializer

    @login_throttle
    def post(self, data, error):
        if error is not None:
            return Response(
                data=error, status=status.HTTP_200_OK
            )
        return Response(
            data=data, status=status.HTTP_400_BAD_REQUEST
        )



class GetMeApiView(GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        return Response(data={
            "message": "ok", "data": {
                "phone_number": str(request.user.phone_number),
                "email": request.user.email
            }
        })
