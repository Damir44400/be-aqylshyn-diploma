from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common import mixins as common_mixins, enums
from apps.general_english import serializers as module_serializers
from apps.general_english.services import module_submit


@extend_schema(tags=["general-english modules submits"])
class ModuleSubmitsView(
    common_mixins.ActionSerializerMixin,
    viewsets.GenericViewSet
):
    serializers = {
        'submit_reading': module_serializers.ModuleOptionSubmitSerializer,
        'submit_listening': module_serializers.ModuleOptionSubmitSerializer,
        'submit_speaking': module_serializers.ModuleSpeakingSubmitSerializer,
        'submit_writing': module_serializers.ModuleWritingSubmitSerializer,
    }

    service = module_submit.ModuleSubmitService()

    def _handle_module_submission(self, request, module_id, submit_method, success_message, type):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = serializer.validated_data
            data['section_name'] = type
            result = submit_method(
                data=data,
                module_id=module_id
            )

            if isinstance(result, (int, float)):
                return Response({
                    "score": result,
                    "message": success_message
                }, status=status.HTTP_200_OK)
            elif result is None:
                return Response({
                    "error": "Failed to submit section"
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "task_id": result,
                    "message": f"{success_message}. Check task status."
                }, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            raise e

    @action(detail=False, methods=['post'], url_path='(?P<module_id>\d+)/reading')
    def submit_reading(self, request, module_id):
        return self._handle_module_submission(
            request,
            module_id,
            self.service.submit_option_answers,
            "Reading section submitted successfully",
            enums.ModuleSectionType.READING
        )

    @action(detail=False, methods=['post'], url_path='(?P<module_id>\d+)/listening')
    def submit_listening(self, request, module_id):
        return self._handle_module_submission(
            request,
            module_id,
            self.service.submit_option_answers,
            "Listening section submitted successfully",
            enums.ModuleSectionType.LISTENING
        )

    @action(detail=False, methods=['post'], url_path='(?P<module_id>\d+)/speaking')
    def submit_speaking(self, request, module_id):
        return self._handle_module_submission(
            request,
            module_id,
            self.service.submit_speaking_answers,
            "Speaking section submitted successfully",
            enums.ModuleSectionType.SPEAKING
        )

    @action(detail=False, methods=['post'], url_path='<module_id>/writing')
    def submit_writing(self, request, module_id):
        return self._handle_module_submission(
            request,
            module_id,
            self.service.submit_writing_answers,
            "Writing section submitted successfully",
            enums.ModuleSectionType.WRITING
        )
