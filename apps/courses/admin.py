from django.contrib import admin
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.common import enums as common_enums
from apps.courses import models
from apps.courses.admin_page import views as admin_views


# Register your models here.
@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration', 'has_level_define', "type", 'create_test_link')
    search_fields = ('name', 'description')
    list_filter = ('has_level_define',)

    fieldsets = (
        (None, {
            'fields': ('name', 'duration', "type")
        }),
        (_("Қосымша ақпарат"), {
            'fields': ('description', 'has_level_define'),
            'classes': ('collapse',)
        }),
    )

    def create_test_link(self, obj):
        if obj.type == common_enums.CourseType.GENERAL_ENGLISH:
            url = reverse("admin:create_tests_for_course", args=[obj.pk])
            return format_html('<a href="{}">Create Tests for {}?</a>', url, obj.name)
        else:
            return ""

    create_test_link.short_description = "Create Tests"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<int:course_id>/create-tests/",
                 admin_views.CreateTestAdmin.as_view(),
                 name="create_tests_for_course"),
        ]
        return custom_urls + urls
