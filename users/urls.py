from django.urls import path
from .import views

urlpatterns = [
    path("sign-up/", views.UserSignUp.as_view()),
    path("verify-otp/", views.UserOTP_Verify.as_view()),
    path("sign-in/", views.UserLogin.as_view()),
    path("profile/", views.UserProfile.as_view()),

]
