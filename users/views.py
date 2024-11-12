from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, UserAddress
import random
from .services import send_otp_to_mail
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes


class UserSignUp(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)
        if data.is_valid(raise_exception=True):
            valid_data = data.validated_data
            valid_data.pop("confirm_password")
            password = valid_data.pop("password")
            user = User.objects.create(
                **valid_data,
                otp=random.randint(1000, 9999),
                password=password
            )
            user.set_password(password)
            user.is_active = False
            user.save()
            send_otp_to_mail(username=f"{user.first_name} {user.last_name}", otp=user.otp, user_email=user.email)
            serialize = self.serializer_class(user)
            return Response({"status": "user registered successfully", "data": serialize.data}, status.HTTP_201_CREATED)


class UserOTP_Verify(generics.CreateAPIView):
    serializer_class = UserVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)
        if data.is_valid(raise_exception=True):
            usr = data.validated_data['email']
            otp = data.validated_data['otp']
            resend = self.request.query_params.get("resend")
            if str(resend).lower() == "true":
                send_otp_to_mail(username=usr.username, otp=usr.otp, user_email=usr.email)
                return Response({"status": "OTP send successfully"})
            if usr.otp == otp:
                usr.is_active = True
                usr.save()
                return Response({
                    "status": "user verified successfully",
                })

            return Response({
                "status": "Invalid otp please check again."
            }, status=status.HTTP_404_NOT_FOUND)


class UserLogin(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)
        if data.is_valid(raise_exception=True):
            user = data.validated_data['user']
            user_auth = authenticate(email=user.email, password=data.validated_data['password'])
            if user_auth:
                token, created = Token.objects.get_or_create(user=user)
                user_data = UserSerializer(user)
                return Response(
                    {'token': token.key, "status": "user login successfully.", "user_details": user_data.data},
                    status=status.HTTP_200_OK)
            return Response({"password": "login failed due to invalid password."}, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(generics.ListAPIView, generics.UpdateAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        uid = request.query_params.get("id")
        if uid is not None:
            try:
                user = User.objects.get(id=uid)
                serialize = self.serializer_class(user)
            except Exception as e:
                print(f"error at get user profile: {e}")
                return Response({"status": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serialize = self.serializer_class(request.user)
        return Response(serialize.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        uid = request.query_params.get("id")
        if uid is None or uid == "":
            return Response({"status": "Invalid user id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=uid)
        except Exception as e:
            print(f"error at update user profile: {e}")
            return Response({"status": "user not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserAddressView(generics.ListCreateAPIView, generics.UpdateAPIView,
                      generics.DestroyAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def handle_default_address(usr):
        user_address = UserAddress.objects.filter(is_default=True, user=usr)
        if user_address.exists() is True:
            usr_address = user_address.first()
            usr_address.is_default = False
            usr_address.save()

    def post(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)
        if data.is_valid(raise_exception=True):
            if data.validated_data.get("is_default") is True:

                self.handle_default_address(usr=data.validated_data['user'])

            user_address = UserAddress.objects.create(
                **data.validated_data
            )
            serialize = self.serializer_class(user_address)
            return Response(serialize.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        user_mail = request.query_params.get("user")
        user_address = UserAddress.objects.select_related("user").filter(user__email=user_mail)
        serialize = self.serializer_class(user_address, many=True)
        return Response(serialize.data)

    def patch(self, request, *args, **kwargs):
        address_id = request.query_params.get("id")
        user_address = UserAddress.objects.filter(id=address_id)
        if user_address.exists():
            serializer = self.serializer_class(user_address.first(), data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                if serializer.validated_data.get("is_default") is True:
                    self.handle_default_address(usr=serializer.validated_data['user'])
                serializer.save()
            return Response(serializer.data)
        return Response({"id": "address not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        address_id = request.query_params.get("id")
        user_address = UserAddress.objects.get(id=address_id)
        user_address.delete()
        return Response({"status": "address deleted successfully"})


@api_view(['POST'])
@permission_classes([AllowAny])
def send_forget_otp(request):
    usr = User.objects.filter(email=request.data.get('email')).first()
    if usr:
        usr.otp = random.randint(1000, 9999)
        usr.save()
        send_otp_to_mail(username=f"{usr.first_name} {usr.last_name}", otp=usr.otp, user_email=usr.email)
        return Response({"status": "otp send successfully"})
    return Response({"status": "user does not exits. please check email."})


class SetUserPassword(generics.CreateAPIView):
    serializer_class = SetUserPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)
        if data.is_valid(raise_exception=True):
            usr = data.validated_data['user']
            usr.set_password(data.validated_data['password'])
            usr.save()
            return Response({"status": "password change successfully."})


