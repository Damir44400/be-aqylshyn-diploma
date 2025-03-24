from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.general_english import models as general_english_models


class Speaking(models.Model):
    context = models.CharField(max_length=255)
    module = models.ForeignKey(
        general_english_models.Module,
        on_delete=models.CASCADE,
        verbose_name=_("Қай модульге тиесілі"),
        related_name="speakings",
    )
