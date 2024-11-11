from django.contrib import admin
from .models import User
from import_export.admin import ImportExportModelAdmin


class user(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["username", "email", "is_superuser", "is_active", "gender"]
    list_filter = ["is_superuser", "is_active"]
    search_fields = ["email", "username"]


admin.site.register(User, user)
