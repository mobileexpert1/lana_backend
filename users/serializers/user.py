from rest_framework import serializers
from users.models import User
from rest_framework.serializers import ValidationError
from django.db.models import Q
import re


class UserSignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255, required=True, write_only=True)
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=True, max_length=10, min_length=10,
                                         error_messages={
                                             'required': 'Phone number is required.',
                                             'max_length': 'Phone number must be exactly 10 digits.',
                                             'min_length': 'Phone number must be exactly 10 digits.',
                                             'invalid': 'Invalid phone number format.'
                                         }
                                         )

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "email", "gender", "password", "confirm_password", "phone_number")

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs['confirm_password']
        if password != confirm_password:
            raise ValidationError({"confirm_password": "password does not match."})

        email = attrs.get("email")
        attrs['email'] = email.lower()

        return attrs

    @staticmethod
    def validate_phone_number(value):
        phone_regex = re.compile(r'^[6-9]\d{9}$')
        if not phone_regex.match(value):
            raise serializers.ValidationError(
                'Invalid phone number format. It should start with a digit between 6 and 9 and be 10 digits long.')
        elif User.objects.filter(phone_number=value).exists() is True:
            raise serializers.ValidationError(
                'mobile number already exits.')
        return value


class UserVerifySerializer(serializers.Serializer):
    otp = serializers.IntegerField(
        min_value=1000, max_value=9999,
        error_messages={
            'min_value': 'OTP must be a 4-digit number.',
            'max_value': 'OTP must be a 4-digit number.',
            'invalid': 'Invalid OTP. Please enter a valid 4-digit number.'
        }
    )
    email = serializers.CharField(max_length=255)

    def validate(self, attrs):
        email = attrs.get("email")
        user = User.objects.filter(email=email)
        if user.exists() is False:
            raise ValidationError({"email": "Invalid username and email."})
        # elif user.first().is_active is True:
        #     raise ValidationError({"email": "user already verified."})
        attrs['email'] = user.first()
        return attrs


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.filter(email=attrs.get("email"))
        if user.exists() is False:
            raise serializers.ValidationError(
                {"email": "user does not exists. please check email"})

        elif user.first().is_active is False:
            raise serializers.ValidationError({"email": "user is not verified."})

        attrs['user'] = user.first()

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "profile_pic", "gender", "id", "phone_number",)


class SetUserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)
    email = serializers.EmailField()

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs['confirm_password']
        if password != confirm_password:
            raise ValidationError({"confirm_password": "password does not match."})

        usr = User.objects.filter(email=attrs.get("email"))
        if usr.exists() is False:
            raise ValidationError({"email": "email does not exits."})
        attrs['user'] = usr.first()
        return attrs



