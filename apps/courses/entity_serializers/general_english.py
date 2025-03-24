from rest_framework import serializers

from apps.courses import models as courses_models
from apps.courses import serializers as course_serializers
from apps.general_english import serializers as general_english_serializers


class CourseGeneralEnglishRetrieveSerializer(course_serializers.CourseSerializer):
    last_module = serializers.SerializerMethodField()
    user_course = serializers.SerializerMethodField()

    class Meta(course_serializers.CourseSerializer.Meta):
        fields = course_serializers.CourseSerializer.Meta.fields + (
            "description",
            "duration",
            "last_module",
            "user_course"
        )

    def get_last_module(self, obj):
        user = self.context['request'].user
        user_course = None
        if hasattr(obj, 'user_course'):
            user_course = obj.user_course.filter(user=user).first()
        return user_course.last_module if user_course else None

    def get_user_course(self, obj):
        user = self.context['request'].user
        if hasattr(obj, 'user_course'):
            user_course = obj.user_course.filter(user=user).first()
            return user_course.get_progress if user_course else None
        return None


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

    def get_modules(self, obj):
        user = self.context['request'].user
        if hasattr(obj, 'user_course'):
            user_course = obj.user_course.filter(user=user).first()
            if user_course:
                modules_qs = user_course.user_modules.all()
                return general_english_serializers.ModuleSerializer(modules_qs, many=True).data
        return None
