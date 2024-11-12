from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/", include("users.urls")),
    path("", include("dashboard.urls"))
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

