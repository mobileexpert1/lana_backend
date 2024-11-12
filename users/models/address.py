from django.db import models
from common.models import CommonFields


class UserAddress(CommonFields):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)



