from typing import Any, Dict, Union, Optional, Callable

from drf_spectacular import openapi
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.common import mixins as common_mixins, enums
from apps.general_english import serializers as module_serializers
from apps.general_english.services import module_submit


@extend_schema(tags=["general-english modules submits"])
class ModuleSubmitsView(
    common_mixins.ActionSerializerMixin,
    viewsets.GenericViewSet
):
    """ViewSet to handle module submissions for different sections (reading, listening, speaking, writing)."""

    serializers = {
        'submit_reading': module_serializers.ModuleOptionSubmitSerializer,
        'submit_listening': module_serializers.ModuleOptionSubmitSerializer,
        'submit_speaking': module_serializers.ModuleSpeakingSubmitSerializer,
        'submit_writing': module_serializers.ModuleWritingSubmitSerializer,
        "get_score": module_serializers.ModuleScoreSerializer
    }

    service = module_submit.ModuleSubmitService()
    permission_classes = [permissions.IsAuthenticated]

    def _handle_module_submission(
            self,
            request: Request,
            module_id: int,
            submit_method: Callable,
            success_message: str,
            section_type: str
    ) -> Response:
        """
        Common handler for all module section submissions.

        Args:
            request: The HTTP request object
            module_id: ID of the module being submitted
            submit_method: Service method to call for submission processing
            success_message: Message to return on successful submission
            section_type: Type of section being submitted

        Returns:
            Response with appropriate status code and data
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = serializer.validated_data
            data['section_name'] = section_type

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

        except ValueError as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Submit answers for the reading section of a module",
        responses={
            200: openapi.OpenApiResponse(description="Reading section submitted successfully"),
            202: openapi.OpenApiResponse(description="Reading section processing asynchronously"),
            400: openapi.OpenApiResponse(description="Invalid submission data")
        }
    )
    @action(detail=False, methods=['post'], url_path='(?P<module_id>\d+)/reading')
    def submit_reading(self, request: Request, module_id: int) -> Response:
        """Submit answers for the reading section of a module."""
        return self._handle_module_submission(
            request,
            module_id,
            self.service.submit_option_answers,
            "Reading section submitted successfully",
            enums.ModuleSectionType.READING
        )

    @extend_schema(
        description="Submit answers for the listening section of a module",
        responses={
            200: openapi.OpenApiResponse(description="Listening section submitted successfully"),
            202: openapi.OpenApiResponse(description="Listening section processing asynchronously"),
            400: openapi.OpenApiResponse(description="Invalid submission data")
        }
    )
    @action(detail=False, methods=['post'], url_path='(?P<module_id>\d+)/listening')
    def submit_listening(self, request: Request, module_id: int) -> Response:
        """Submit answers for the listening section of a module."""
        return self._handle_module_submission(
            request,
            module_id,
            self.service.submit_option_answers,
            "Listening section submitted successfully",
            enums.ModuleSectionType.LISTENING
        )

    @extend_schema(
        description="Submit answers for the speaking section of a module",
        responses={
            200: openapi.OpenApiResponse(description="Speaking section submitted successfully"),
            202: openapi.OpenApiResponse(description="Speaking section processing asynchronously"),
            400: openapi.OpenApiResponse(description="Invalid submission data")
        }
    )
    @action(detail=False, methods=['post'], url_path='(?P<module_id>\d+)/speaking')
    def submit_speaking(self, request: Request, module_id: int) -> Response:
        """Submit answers for the speaking section of a module."""
        return self._handle_module_submission(
            request,
            module_id,
            self.service.submit_speaking_answers,
            "Speaking section submitted successfully",
            enums.ModuleSectionType.SPEAKING
        )

    @extend_schema(
        description="Submit answers for the writing section of a module",
        responses={
            200: openapi.OpenApiResponse(description="Writing section submitted successfully"),
            202: openapi.OpenApiResponse(description="Writing section processing asynchronously"),
            400: openapi.OpenApiResponse(description="Invalid submission data")
        }
    )
    @action(detail=False, methods=['post'], url_path='(?P<module_id>\d+)/writing')
    def submit_writing(self, request: Request, module_id: int) -> Response:
        """Submit answers for the writing section of a module."""
        return self._handle_module_submission(
            request,
            module_id,
            self.service.submit_writing_answers,
            "Writing section submitted successfully",
            enums.ModuleSectionType.WRITING
        )

    @extend_schema(
        parameters=[
            openapi.OpenApiParameter(
                name='section_name',
                type=openapi.OpenApiTypes.STR,
                enum=enums.ModuleSectionType.values,
                description="The section name to get the score for"
            )
        ],
        responses={
            200: module_serializers.ModuleScoreSerializer,
            404: openapi.OpenApiResponse(description="Score not found")
        },
        description="Get the score for a specific module section"
    )
    @action(detail=False, methods=['get'], url_path='(?P<module_id>\d+)/get-score')
    def get_score(self, request: Request, module_id: int) -> Response:
        """Retrieve the score for a specific module section."""
        try:
            data = self.service.get_score(request, module_id)
            return Response(data)
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve score: {str(e)}"},
                status=status.HTTP_404_NOT_FOUND
            )