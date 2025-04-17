import django_filters

from .models import University


class UniversityFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name="id")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    fields_of_study = django_filters.BaseInFilter(field_name="fields_of_study__id", lookup_expr="in")
    languages = django_filters.CharFilter(field_name="languages__id", lookup_expr="icontains")
    study_formats = django_filters.CharFilter(field_name="study_formats__id", lookup_expr="icontains")

    class Meta:
        model = University
        fields = [
            "id",
            "name",
            "location",
            "degree_type",
            "duration",
            "languages",
            "study_formats",
            "fields_of_study",
        ]
