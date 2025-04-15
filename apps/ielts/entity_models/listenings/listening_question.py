from django.db import models

from apps.common import enums
from apps.common.models import BaseModel
from .listening import IeltsListening


class IeltsListeningQuestion(BaseModel):
    listening = models.ForeignKey(
        IeltsListening,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_content = models.TextField(verbose_name='Question Text')

    question_type = models.CharField(
        max_length=32,
        choices=enums.IeltsListeningQuestionType.choices,
        default=enums.IeltsListeningQuestionType.OPTIONS,
        verbose_name='Question Type'
    )

    def __str__(self):
        return f"Question #{self.id} - {self.get_question_type_display()}"


    class Meta:
        verbose_name_plural = "Listening | Questions"