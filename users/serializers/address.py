from rest_framework import serializers
from users.models import UserAddress, User


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(write_only=True)

    class Meta:
        model = UserAddress
        fields = ("id", "street", "city", "state", "is_default", "user")

    def validate(self, attrs):
        email = attrs.get("user")
        usr = User.objects.filter(email=email)
        if usr.exists() is False:
            raise serializers.ValidationError({"user": "user does not exits."})
        attrs['user'] = usr.first()

        return attrs


