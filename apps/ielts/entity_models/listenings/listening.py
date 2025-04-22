from django.db import models

from apps.common import enums
from ..ielts_test import IeltsTest


class IeltsListening(models.Model):
    title = models.CharField()
    audio_file = models.FileField()
    part = models.PositiveSmallIntegerField(
        choices=enums.IELTSListeningPart.choices,
        default=enums.IELTSListeningPart.PART1,
        verbose_name='Бөлім (Part)',
    )
    test = models.OneToOneField(IeltsTest, on_delete=models.CASCADE, related_name='listening_part')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Listening | Audios"
