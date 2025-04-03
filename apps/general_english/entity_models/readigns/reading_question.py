from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.general_english import models as general_english_models


class ReadingQuestion(models.Model):
    context = models.TextField(_("Оқу мәтіні"), help_text=_("Бұл сұрақ қатысты мәтін үзіндісі"))
    image = models.URLField(_("Сурет сілтемесі"), null=True, blank=True)
    source = models.TextField(_("Дереккөз"), blank=True, null=True)
    module = models.ForeignKey(
        general_english_models.Module,
        on_delete=models.CASCADE,
        verbose_name=_("Қай модульге тиесілі"),
        related_name="readings"
    )
