from django.urls import path
from .import views


urlpatterns = [
    path("cart-producti/", views.ProductCartInfo.as_view()),

]

