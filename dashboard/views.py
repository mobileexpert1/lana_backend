from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import CardLinkSerializer
from .services import get_card_product


class ProductCartInfo(generics.CreateAPIView):
    serializer_class = CardLinkSerializer

    def post(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)
        if data.is_valid(raise_exception=True):
            products = get_card_product(data.validated_data['link'])
            if len(products) == 0:
                products = get_card_product(data.validated_data['link'])
            return Response({"statis": "ok",
                             "products": products})




