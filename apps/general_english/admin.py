from django.contrib import admin

from apps.general_english import models


@admin.register(models.TrialQuestion)
class TrialQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'question_type', 'course')
    list_filter = ('course', 'question_type')
    search_fields = ('question', 'course__name')

    fieldsets = (
        (None, {
            'fields': ('question', 'question_type', 'course')
        }),
    )


@admin.register(models.TrialOption)
class TrialOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'option', 'is_correct', 'question')
    list_filter = ('is_correct', 'question__course')
    search_fields = ('option', 'question__question')

    fieldsets = (
        (None, {
            'fields': ('question', 'option', 'is_correct')
        }),
    )
