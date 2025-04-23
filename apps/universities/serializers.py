from rest_framework import serializers

from .favorites.models import Favorite
from .models import (
    FieldsOfStudy,
    Location,
    DegreeType,
    Language,
    StudyFormat,
    Duration,
    University,
)


class FieldsOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldsOfStudy
        fields = ('id', 'name', 'tuition_fee')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name')


class DegreeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DegreeType
        fields = ('id', 'name')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name')


class StudyFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyFormat
        fields = ('id', 'name')


class DurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = ('id', 'duration', 'prefix')


class UniversityListSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = University
        fields = (
            'id',
            'name',
            "image",
            'duration',
            'pace',
            'location',
            'languages',
            'description',
            'is_favorite',
        )

    def get_location(self, obj):
        return obj.location.name if obj.location else None

    def get_duration(self, obj):
        return f"{obj.duration.duration} {obj.duration.prefix}" if obj.duration else None

    def get_languages(self, obj):
        return [language.name for language in obj.languages.all()]

    def get_description(self, obj):
        return obj.key_summary[:50] if obj.key_summary else None

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if not request or user.is_anonymous:
            return False
        favorite = Favorite.objects.filter(user=user, university=obj)
        return True if favorite else False


class UniversityDetailSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    languages = LanguageSerializer(many=True)
    study_formats = StudyFormatSerializer(many=True)
    duration = DurationSerializer()
    degree_type = DegreeTypeSerializer()
    fields_of_study = FieldsOfStudySerializer(many=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = University
        fields = (
            'id',
            'name',
            'image',
            'about',
            'logo',
            'is_favorite',
            'languages',
            'study_formats',
            'duration',
            'location',
            'degree_type',
            'fields_of_study',
            'key_summary',
            'introduction',
            'academic_requirements',
            'scholarships_funding',
            'tuition_fees',
            'pace',
            'application_deadline',
        )

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if not request or user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, university=obj).exists()
