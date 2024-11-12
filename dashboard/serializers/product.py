from rest_framework import serializers


class CardLinkSerializer(serializers.Serializer):
    link = serializers.URLField()

    def validate(self, attrs):
        url = attrs.get("link")
        base_url = "http://api-shein.shein.com/"
        if url.startswith(base_url) is False and url.startswith("https://api-shein.shein.com/") is False:
            raise serializers.ValidationError({"link": "invalid link or it does not exits to Shein."})

        return attrs

