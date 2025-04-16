from rest_framework import serializers

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
        )

    def get_location(self, obj):
        return obj.location.name if obj.location else None

    def get_duration(self, obj):
        return f"{obj.duration.duration} {obj.duration.prefix}" if obj.duration else None

    def get_languages(self, obj):
        return [language.name for language in obj.languages.all()]

    def get_description(self, obj):
        return obj.key_summary[:50] if obj.key_summary else None


class UniversityDetailSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    languages = LanguageSerializer(many=True)
    study_formats = StudyFormatSerializer(many=True)
    duration = DurationSerializer()
    degree_type = DegreeTypeSerializer()
    fields_of_study = FieldsOfStudySerializer(many=True)

    class Meta:
        model = University
        fields = '__all__'
