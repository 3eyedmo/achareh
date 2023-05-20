from rest_framework.exceptions import APIException

class RegisterationEmailOrPhoneExists(APIException):
    status_code=403
    default_code="error"


class PhoneOrPasswordWrong(APIException):
    status_code=403
    default_code="error"


class BannedUser(APIException):
    status_code=403
    default_code="error"
    default_detail="you are banned."