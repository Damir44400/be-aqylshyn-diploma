from django.db import models

from apps.common import enums
from apps.ielts import models as ielts_models


class IeltsSpeakingPart(models.Model):
    part = models.PositiveSmallIntegerField(
        choices=enums.IELTSSpeakingPart.choices,
        default=enums.IELTSSpeakingPart.PART1
    )
    test = models.ForeignKey(ielts_models.IeltsTest, on_delete=models.CASCADE, related_name='speaking_parts')

    class Meta:
        unique_together = ('test', 'part')
        verbose_name_plural = "Speaking | Parts"

    def __str__(self):
        return f'{self.test} - {self.part}'
