from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid


class UserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email is required."))
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, email, **extra_fields):
        if not email:
            raise ValueError(_("Email is required."))
        extra_fields.setdefault("is_active", True)
        user = self.create_user(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    gender_choice = (
        ("male", "male"),
        ("female", "female"),
        ("others", "others")
    )
    id = models.CharField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, max_length=255)
    profile_pic = models.ImageField(upload_to="profile", null=True, blank=True)
    gender = models.CharField(max_length=20, choices=gender_choice, default="male")
    email = models.EmailField(unique=True)
    is_set_password = models.BooleanField(default=True)
    otp = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    username = None

    REQUIRED_FIELDS = ["password"]
    USERNAME_FIELD = "email"
    objects = UserManager()
