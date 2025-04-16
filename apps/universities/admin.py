from django.contrib import admin

from .models import (
    FieldsOfStudy,
    Location,
    DegreeType,
    Language,
    StudyFormat,
    Duration,
    University,
)


@admin.register(FieldsOfStudy)
class FieldsOfStudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'tuition_fee')
    search_fields = ('name',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(DegreeType)
class DegreeTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(StudyFormat)
class StudyFormatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Duration)
class DurationAdmin(admin.ModelAdmin):
    list_display = ('duration', 'prefix')
    search_fields = ('prefix',)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'degree_type')
    search_fields = ('name',)
    list_filter = ('location', 'degree_type', 'languages')
    filter_horizontal = ('languages', 'study_formats', 'fields_of_study',)
