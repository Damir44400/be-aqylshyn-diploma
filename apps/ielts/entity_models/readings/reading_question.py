from django.db import models

from apps.common import enums
from apps.common.models import BaseModel
from .reading import IeltsReading


class IeltsReadingQuestion(BaseModel):
    reading = models.ForeignKey(
        IeltsReading,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Оқу мәтіні'
    )
    question_content = models.TextField(verbose_name='Question Text')

    question_type = models.CharField(
        max_length=32,
        choices=enums.IeltsReadingQuestionType.choices,
        default=enums.IeltsReadingQuestionType.OPTIONS,
        verbose_name='Question Type'
    )

    def __str__(self):
        return f"Question #{self.id} - {self.get_question_type_display()}"
