from django.contrib.postgres.fields import ArrayField
from django.db import models


class FieldsOfStudy(models.Model):
    name = models.CharField("Атауы", max_length=100)
    tuition_fee = models.DecimalField("Оқу құны", decimal_places=2, max_digits=10,
                                      help_text="Оқу құны, мысалы: 150000.00")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Оқу аумағы"


class Location(models.Model):
    name = models.CharField("Атауы", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Орналасқан жері"


class DegreeType(models.Model):
    name = models.CharField("Атауы", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Оқу дәрежесі"


class Language(models.Model):
    name = models.CharField("Атауы", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Оқыту тілі"


class StudyFormat(models.Model):
    name = models.CharField("Атауы", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Оқыту форматы"


class Duration(models.Model):
    duration = models.IntegerField("Мерзімі", help_text="Мерзімді санмен енгізіңіз")
    prefix = models.CharField("Бірлік", max_length=100, help_text="Мысалы: ай, жыл")

    def __str__(self):
        return f"{self.duration} {self.prefix}"

    class Meta:
        verbose_name_plural = "Оқыту ұзақтығы"


class University(models.Model):
    name = models.CharField("Аты", max_length=100)
    image = models.ImageField("Университет суреты", upload_to="university_images/", blank=True, null=True)
    about = models.TextField("Университет туралы", blank=True, null=True)
    logo = models.ImageField("Логотип", upload_to='university_logos/', blank=True, null=True)

    # Связанные модели
    languages = models.ManyToManyField(Language, blank=True, verbose_name="Оқыту тілдері")
    study_formats = models.ManyToManyField(StudyFormat, blank=True, verbose_name="Оқыту форматы")
    duration = models.ForeignKey(Duration, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="Оқыту ұзақтығы")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="Орналасқан жері")
    degree_type = models.ForeignKey(DegreeType, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name="Оқу дәрежесі")
    fields_of_study = models.ManyToManyField(FieldsOfStudy, blank=True, verbose_name="Оқу аумағы")

    # Поля для детальной страницы
    key_summary = models.TextField("Қысқаша шолу", blank=True, null=True)
    introduction = models.TextField("Кіріспе", blank=True, null=True)
    academic_requirements = models.TextField("Академиялық талаптар", blank=True, null=True)
    scholarships_funding = models.TextField("Стипендия және қаржыландыру", blank=True, null=True)
    tuition_fees = models.CharField(null=True)
    pace = models.CharField(default="Full Time")
    application_deadline = models.CharField(null=True)
    
    study_highlights = ArrayField(
        models.TextField(),
        verbose_name="Мұнда оқу нені білдіреді?",
        blank=True,
        null=True,
    )
    program_benefits = ArrayField(
        models.TextField(),
        verbose_name="Неге бұл бағдарламаны таңдау керек?",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Университеттер"
