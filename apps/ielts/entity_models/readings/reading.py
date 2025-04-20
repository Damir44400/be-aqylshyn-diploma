from django.db import models

from apps.common import models as common_models, enums
from ..ielts_test import IeltsTest


class IeltsReading(common_models.BaseModel):
    title = models.CharField(max_length=255, verbose_name='Мәтіннің атауы')
    content = models.TextField(verbose_name='Мәтін')
    passage_number = models.PositiveSmallIntegerField(
        choices=enums.IELTSReadingPassage.choices,
        default=enums.IELTSReadingPassage.PASSAGE_1,
    )
    test = models.ForeignKey(IeltsTest, on_delete=models.CASCADE, related_name='reading_passages')

    class Meta:
        verbose_name_plural = "Reading | Passages"

    def __str__(self):
        return self.title
