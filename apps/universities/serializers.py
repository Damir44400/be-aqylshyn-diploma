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
    location = LocationSerializer()

    class Meta:
        model = University
        fields = ('id', 'name', 'website', 'location')


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
