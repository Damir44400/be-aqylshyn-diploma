from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.general_english import models as general_english_models


class TrialOption(models.Model):
    question = models.ForeignKey(
        general_english_models.TrialQuestion,
        on_delete=models.CASCADE,
        verbose_name=_("Қай сұраққа тиесілі"),
        related_name="trial_options",
    )
    option = models.CharField(
        max_length=200,
        verbose_name=_("Опция")
    )

    is_correct = models.BooleanField(default=False, verbose_name=_("Бұл дұрыс опцияма?"))

    def __str__(self):
        return self.option

    class Meta:
        verbose_name = _("Сынама сұрақ опциясы")
        verbose_plural_name = _("Сынама сұрақ опциялары")
