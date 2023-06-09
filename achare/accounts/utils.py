from rest_framework_simplejwt.tokens import RefreshToken


def get_token_pair(user):
    refresh = RefreshToken.for_user(user=user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }