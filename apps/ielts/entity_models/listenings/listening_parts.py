from django.db import models

from apps.common import enums
from apps.ielts import models as ielts_models


class IeltsListeningPart(models.Model):
    part = models.PositiveSmallIntegerField(
        choices=enums.IELTSListeningPart.choices,
        default=enums.IELTSListeningPart.PART1,
        verbose_name='Бөлім (Part)',
    )
    listening = models.ForeignKey(ielts_models.IeltsListening, on_delete=models.CASCADE, related_name='listening_parts')

    def __str__(self):
        return f"{self.part}-{self.listening}"

    class Meta:
        verbose_name_plural = "Listening | Parts"
        unique_together = ('part', 'listening')