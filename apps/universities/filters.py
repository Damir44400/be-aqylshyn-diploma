import django_filters
from django.db.models import Q

from apps.universities.models import University


class UniversityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    location = django_filters.CharFilter(method="filter_location")
    degree_type = django_filters.CharFilter(method="filter_degree_type")
    duration = django_filters.CharFilter(method="filter_duration")
    languages = django_filters.CharFilter(method="filter_languages")
    study_formats = django_filters.CharFilter(method="filter_study_formats")
    fields_of_study = django_filters.CharFilter(method="filter_fields_of_study")

    def filter_location(self, queryset, name, value):
        return queryset.filter(location__name__icontains=value)

    def filter_degree_type(self, queryset, name, value):
        return queryset.filter(degree_type__name__icontains=value)

    def filter_duration(self, queryset, name, value):
        return queryset.filter(
            Q(duration__duration__icontains=value) | Q(duration__prefix__icontains=value)
        )

    def filter_languages(self, queryset, name, value):
        return queryset.filter(languages__name__icontains=value)

    def filter_study_formats(self, queryset, name, value):
        return queryset.filter(study_formats__name__icontains=value)

    def filter_fields_of_study(self, queryset, name, value):
        return queryset.filter(fields_of_study__name__icontains=value)

    class Meta:
        model = University
        fields = [
            "name",
            "location",
            "degree_type",
            "duration",
            "languages",
            "study_formats",
            "fields_of_study",
        ]
