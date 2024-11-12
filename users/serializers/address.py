from rest_framework import serializers
from users.models import UserAddress


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ("id", "street", "city", "state", "is_default")

