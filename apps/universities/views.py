from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import UniversityFilter
from .models import (
    University,
    Location,
    Language,
    StudyFormat,
    DegreeType,
    FieldsOfStudy,
)
from .serializers import (
    UniversityListSerializer,
    UniversityDetailSerializer,
    LocationSerializer,
    LanguageSerializer,
    StudyFormatSerializer,
    DegreeTypeSerializer,
    FieldsOfStudySerializer,
)
from ..common.mixins import ActionSerializerMixin


class UniversityViewSet(
    ActionSerializerMixin,
    viewsets.ReadOnlyModelViewSet
):
    queryset = University.objects.all().prefetch_related(
        "languages", "study_formats", "fields_of_study"
    ).select_related("duration", "location", "degree_type")
    serializers = {
        'list': UniversityListSerializer,
        'retrieve': UniversityDetailSerializer,
        "locations": LocationSerializer,
        "languages": LanguageSerializer,
        "study_formats": StudyFormatSerializer,
        "degree_types": DegreeTypeSerializer,
        "fields_of_study": FieldsOfStudySerializer,
    }
    filter_backends = [DjangoFilterBackend]
    filterset_class = UniversityFilter

    @action(detail=False, methods=['get'], url_path='locations')
    def locations(self, request, *args, **kwargs):
        queryset = Location.objects.all()
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='languages')
    def languages(self, request, *args, **kwargs):
        queryset = Language.objects.all()
        serializer = LanguageSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='study-formats')
    def study_formats(self, request, *args, **kwargs):
        queryset = StudyFormat.objects.all()
        serializer = StudyFormatSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='degree-types')
    def degree_types(self, request, *args, **kwargs):
        queryset = DegreeType.objects.all()
        serializer = DegreeTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='field-studies')
    def field_studies(self, request, *args, **kwargs):
        queryset = FieldsOfStudy.objects.all()
        serializer = FieldsOfStudySerializer(queryset, many=True)
        return Response(serializer.data)
