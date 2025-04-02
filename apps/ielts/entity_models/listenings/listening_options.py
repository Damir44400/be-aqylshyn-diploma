from django.db import models

from .listening_question import IeltsListeningQuestion


class IeltsListeningOption(models.Model):
    question = models.ForeignKey(
        IeltsListeningQuestion,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='Сұрақ'
    )
    option = models.CharField(
        max_length=255,
        verbose_name='Жауап нұсқасы'
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name='Дұрыс жауап па?'
    )

    def __str__(self):
        return f"{self.option} ({'Correct' if self.is_correct else 'Incorrect'})"


class IeltsListeningFillBlank(models.Model):
    question = models.OneToOneField(
        IeltsListeningQuestion,
        on_delete=models.CASCADE,
        related_name='fill_blank',
        verbose_name='Сұрақ'
    )
    answer = models.JSONField(
        verbose_name='Дұрыс жауаптар тізімі',
        help_text="Жауаптар ретімен берілген массив түрінде болады"
    )

    def __str__(self):
        return f"FillBlank for Question #{self.question.id}"
