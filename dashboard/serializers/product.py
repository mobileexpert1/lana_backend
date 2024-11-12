from rest_framework import serializers


class CardLinkSerializer(serializers.Serializer):
    link = serializers.URLField()

    def validate(self, attrs):
        pass

