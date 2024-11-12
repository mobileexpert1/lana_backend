from django.urls import path
from .import views

urlpatterns = [
    path("sign-up/", views.UserSignUp.as_view()),
    path("verify-otp/", views.UserOTP_Verify.as_view()),
    path("sign-in/", views.UserLogin.as_view()),
    path("profile/", views.UserProfile.as_view()),
    path("address/", views.UserAddressView.as_view()),
    path("send-forget-otp/", views.send_forget_otp),
    path("set-password/", views.SetUserPassword.as_view()),

]
