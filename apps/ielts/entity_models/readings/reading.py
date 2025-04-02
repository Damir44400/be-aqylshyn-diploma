from django.db import models

from apps.common import models as common_models
from ..ielts_test import IeltsTest


class IeltsReading(common_models.BaseModel):
    title = models.CharField(max_length=255, verbose_name='Мәтіннің атауы')
    content = models.TextField(verbose_name='Мәтін')
    test = models.ForeignKey(IeltsTest, on_delete=models.CASCADE, related_name='readings')

    class Meta:
        verbose_name = 'Оқу мәтіні'
        verbose_name_plural = 'Оқу мәтіндері'

    def __str__(self):
        return self.title
