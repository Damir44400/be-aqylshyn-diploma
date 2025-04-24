from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common import mixins as common_mixins
from apps.courses import models as courses_models
from apps.courses.entity_serializers import general_english as course_general_english_serializers
from apps.general_english import serializers as general_english_serializers
from apps.general_english.services import trial_test


@extend_schema(tags=["general-english trial test"])
class TrialTestViewSet(
    common_mixins.ActionSerializerMixin,
    common_mixins.ActionPermissionMixin,
    viewsets.GenericViewSet
):
    serializers = {
        "trial_questions": course_general_english_serializers.CourseGeneralEnglishTrialQuestionSerializer,
        "send_answer": general_english_serializers.TrialTestSerializer
    }
    service = trial_test.TrialTestService()
    permissions = {
        "send_answer": (permissions.IsAuthenticated,),
        "trial_questions": (permissions.AllowAny,)
    }

    @action(detail=False, methods=['post'], url_path='course/(?P<course_id>\d+)/send-answer')
    def send_answer(self, request, course_id=None):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        score, user_level = self.service.trial_test_answer_check(course_id, serializer.validated_data, user)

        return Response({"score": score, "user_level": user_level}, status=200)

    @action(detail=False, methods=["get"], url_path="course/(?P<course_id>\d+)/trial-questions")
    def trial_questions(self, request, course_id=None):
        instance = courses_models.Course.objects.filter(id=course_id).first()
        if instance is None:
            return Response(status=404, data={"detail": "Course not found"})
        serializer = self.get_serializer(instance=instance, context={"request": request})
        return Response(serializer.data)
