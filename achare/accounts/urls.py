from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView


app_name="accounts"
urlpatterns = [
    path("phone_number/", views.PhoneNumberApiView.as_view(), name="phone_number"),
    path("otp/", views.OTPPhoneNumberApiView.as_view(), name="otp"),
    path('register/', views.RegisterApiView.as_view(), name="register"),
    path('token_pair/', views.TokenPairApiView.as_view(), name="token_pair"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("access/", TokenRefreshView.as_view(), name="access"),
    path("me/", views.GetMeApiView.as_view(), name="me")
]
