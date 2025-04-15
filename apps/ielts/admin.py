from django.contrib import admin

from apps.ielts.models import admin_models

for model in admin_models:
    admin.site.register(model)