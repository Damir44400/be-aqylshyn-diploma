from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.common import enums
from apps.courses import models as courses_models
from apps.courses import serializers as course_serializers
from apps.general_english import models as general_english_models
from apps.general_english import serializers as general_english_serializers


class CourseGeneralEnglishRetrieveSerializer(course_serializers.CourseSerializer):
    last_module = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()
    last_module_name = serializers.SerializerMethodField()

    class Meta(course_serializers.CourseSerializer.Meta):
        fields = course_serializers.CourseSerializer.Meta.fields + (
            "description",
            "duration",
            "last_module",
            "user_progress",
            "last_module_name",
        )

    def get_last_module(self, obj):
        user = self.context['request'].user
        user_course = obj.user_course.filter(user=user).first() if hasattr(obj, "user_course") else None
        module = user_course.last_module if user_course else None
        return module.id if module else None

    def get_user_progress(self, obj):
        user = self.context['request'].user
        if hasattr(obj, 'user_course'):
            user_course = obj.user_course.filter(user=user).first()
            return user_course.get_progress if user_course else 0
        return None

    def get_last_module_name(self, obj):
        user = self.context['request'].user
        user_course = None
        if hasattr(obj, 'user_course'):
            user_course = obj.user_course.filter(user=user).first()
        last_module = user_course.last_module if user_course else None
        return last_module.name if last_module else None


class CourseGeneralEnglishTrialQuestionSerializer(serializers.ModelSerializer):
    questions = general_english_serializers.TrialQuestionSerializer(many=True, read_only=True, source="trial_questions")

    class Meta:
        model = courses_models.Course
        fields = (
            'id',
            'name',
            'questions',
        )


class CourseGeneralEnglishModuleSerializer(CourseGeneralEnglishRetrieveSerializer):
    modules = serializers.SerializerMethodField()

    class Meta(CourseGeneralEnglishRetrieveSerializer.Meta):
        fields = CourseGeneralEnglishRetrieveSerializer.Meta.fields + (
            "modules",
        )

    @extend_schema_field(general_english_serializers.ModuleSerializer(many=True))
    def get_modules(self, obj):
        user = self.context['request'].user
        if hasattr(obj, 'user_course'):
            user_course = obj.user_course.filter(user=user).first()
            if user_course:
                modules_qs: QuerySet[general_english_models.Module] = user_course.user_modules.all().order_by("id")
                for module in modules_qs:
                    if module.is_completed:
                        continue
                    completed_sections = set(general_english_models.ModuleScore.objects.filter(
                        module=module
                    ).values_list('section', flat=True).distinct())

                    required_sections = {
                        enums.ModuleSectionType.WRITING,
                        enums.ModuleSectionType.READING,
                        enums.ModuleSectionType.SPEAKING,
                        enums.ModuleSectionType.LISTENING,
                    }
                    is_complete = required_sections.issubset(completed_sections)
                    print(f"Module complete: {is_complete}")

                    if is_complete != module.is_completed:
                        module.is_completed = is_complete
                        module.save(update_fields=['is_completed'])
                        print(f"Updated module {module.id} completion to {is_complete}")
                return general_english_serializers.ModuleSerializer(modules_qs, many=True).data
        return None
