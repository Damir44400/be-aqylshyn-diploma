import pandas as pd
from django.core.management.base import BaseCommand

from apps.universities.models import University, FieldsOfStudy, Location, DegreeType, Language, StudyFormat, Duration
from core.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Импорт университетов из CSV'

    def handle(self, *args, **kwargs):
        df = pd.read_csv(BASE_DIR / 'универ жинақталған - Лист1.csv')

        for _, row in df.iterrows():
            location_name = row['Университет, ел, бағдарлама атауы'].split(',')[1].strip()
            location, _ = Location.objects.get_or_create(name=location_name)
            duration_value = 4
            duration, _ = Duration.objects.get_or_create(duration=duration_value, prefix="жыл")

            lang, _ = Language.objects.get_or_create(name="Ағылшын")

            format_, _ = StudyFormat.objects.get_or_create(name="Кампус")
            degree_type, _ = DegreeType.objects.get_or_create(name="Бакалавриат")
            field, _ = FieldsOfStudy.objects.get_or_create(name=row['Бағыт'], defaults={'tuition_fee': 0})
            university_name = row['Университет, ел, бағдарлама атауы'].split('—')[0].strip()

            university, created = University.objects.get_or_create(
                name=university_name,
                defaults={
                    'about': row.get('Introduction', ''),
                    'key_summary': row.get('Толық сипаттама', ''),
                    'academic_requirements': row.get('Академиялық талаптар', ''),
                    'scholarships_funding': row.get('Университет ерекшелігі + Неліктен дәл осы университет', ''),
                    'application_deadline': row.get('Құжат тапсыру мерзімі', ''),
                    'tuition_fees': row.get('Оқу форматы, ақысы, ұзақтығы, тілі', ''),
                }
            )

            university.languages.add(lang)
            university.study_formats.add(format_)
            university.duration = duration
            university.location = location
            university.degree_type = degree_type
            university.save()
            university.fields_of_study.add(field)

            self.stdout.write(self.style.SUCCESS(f"Импортировано: {university.name}"))
