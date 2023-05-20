from rest_framework.permissions import BasePermission
from accounts.tokens import AfterOtpToken

class OTPAuthenticated(BasePermission):
    def has_permission(self, request, view):
        super().has_permission(request, view)
        try:
            token = AfterOtpToken(request.headers.get("OTP-TOKEN"))
            request.user = token.get_identity()
        except:
            return False
        return True


