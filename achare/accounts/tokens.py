from rest_framework_simplejwt.tokens import Token
from datetime import timedelta
import json

class AfterOtpToken(Token):
    token_type = "verify"
    lifetime = timedelta(days=1)
    
    @classmethod
    def for_phone_number(cls, phone_number):
        identity = {
            "phone_number":phone_number
        }
        identity = json.dumps(identity)
        token = cls()
        token['identity'] = identity
        return token
    
    def get_identity(self):
        identity = self.payload.get("identity", None)
        identity = json.loads(identity)
        return identity





def get_token_for_phone_number(phone_number):
    token = AfterOtpToken.for_phone_number(phone_number)
    return str(token)

def get_phone_number_from_token(token):
    after_otp_token = AfterOtpToken(token=token)
    return after_otp_token.get_identity().get("phone_number")