from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.general_english import models as general_english_models


class ReadingQuestion(models.Model):
    question = models.TextField(_("Сұрақ мәтіні"), help_text=_("Оқу сұрағының толық мәтіні"))
    reading = models.ForeignKey(
        general_english_models.Reading,
        on_delete=models.CASCADE,
        related_name="reading_questions"
    )