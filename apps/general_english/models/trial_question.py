from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common import enums as common_enums
from apps.general_english import models as general_english_models


class TrialQuestion(models.Model):
    question = models.CharField(max_length=200, verbose_name=_("Сұрақ мәтіні"))
    question_type = models.CharField(
        choices=common_enums.QuestionType.choices,
        verbose_name=_("Сұрақ типі"),
        default=common_enums.QuestionType.SINGLE_CHOICE
    )

    course = models.ForeignKey(
        general_english_models.Course,
        on_delete=models.CASCADE,
        verbose_name=_("Қай курсқа тиесілі")
    )

    def __str__(self):
        return f"{self.question} ({self.question_type.value})"

    class Meta:
        verbose_name = _("Сынама сұрақ")
        verbose_plural_name = _("Сынама сұрақтар")
