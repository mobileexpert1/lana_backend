from django.contrib import admin
from django.apps import apps
from import_export.admin import ImportExportModelAdmin

models = apps.get_models()
remove_fields = ["created_at", "updated_at", "delete_at"]

skip_models = []

for model in models:
    try:
        model_name = f"Custom{model}Admin"
        all_fields = model._meta.fields
        model_field_names = [f.name for f in all_fields]
        if str(model) in skip_models:
            continue
        if str(model) == "<class 'users.models.User'>":
            model_field_names.remove("password")
            model_field_names.remove("ui_id")

        for field in remove_fields:
            model_field_names.remove(field)


        class model_name(ImportExportModelAdmin, admin.ModelAdmin):
            list_display = model_field_names
            try:
                readonly_fields = ['id']
            except:
                pass

            # try:
            #     list_select_related = (
            #         'user',
            #     )
            # except:
            #     pass


        admin.site.register(model, model_name)
    except:
        pass

admin.site.site_header = "ES Administration"
admin.site.site_title = " ES Supplements"
admin.site.index_title = "ES Supplements"
