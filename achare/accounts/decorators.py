from rest_framework.serializers import Serializer
from accounts.core import cache



def login_throttle(view):
    def decorator(self, request, *args, **kwargs):
        ip = request.META.get("REMOTE_ADDR")
        cache.check_ip_for_login(ip=ip)
        serializer: Serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            phone_number = serializer.validated_data.get("phone_number")
            if phone_number:
                cache.check_phonenumber_for_login(phone_number)
                cache.limit_phone_number_for_login(phone_number)
                cache.limit_ip_for_login(ip)
            data = None
            print(serializer.errors)
            return view(self,data , error=serializer.errors)
        phone_number = str(serializer.validated_data.get("phone_number"))
        
        try:
            token_pair = serializer.get_token()
            cache.check_phonenumber_for_login(phone_number)
            data = {
                "token_pair": token_pair,
                "phone_number": phone_number
            }
            return view(self, data, error=None)
        except Exception as e:
            cache.limit_phone_number_for_login(phone_number)
            cache.limit_ip_for_login(ip)
            raise e

    return decorator
