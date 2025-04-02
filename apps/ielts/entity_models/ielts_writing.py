from django.db import models

from apps.common.models import BaseModel
from .ielts_test import IeltsTest


class IeltsWriting(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Тапсырма атауы')
    description = models.TextField(verbose_name='Сипаттама')

    test = models.ForeignKey(IeltsTest, on_delete=models.CASCADE, related_name='writing', null=True)

    def __str__(self):
        return self.title


class WritingImage(models.Model):
    question = models.ForeignKey(
        IeltsWriting,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Сурет'
    )
    image = models.ImageField(upload_to='ielts_writing/', verbose_name='Сурет')

    def __str__(self):
        return f"Image for Question {self.question.id}"
