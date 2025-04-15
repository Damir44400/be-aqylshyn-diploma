from django.db import models
from .reading_question import IeltsReadingQuestion


class IeltsReadingOption(models.Model):
    question = models.ForeignKey(
        IeltsReadingQuestion,
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

    class Meta:
        verbose_name_plural = "Reading | Options"


class IeltsReadingFillBlank(models.Model):
    question = models.OneToOneField(
        IeltsReadingQuestion,
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

    class Meta:
        verbose_name_plural = "Reading | Fill-in-the-blanks"


class IeltsReadingSelectInsert(models.Model):
    question = models.OneToOneField(
        IeltsReadingQuestion,
        on_delete=models.CASCADE,
        related_name='select_insert_data',
        verbose_name='Сұрақ'
    )

    correct_answer = models.TextField(
        verbose_name='Дұрыс сөйлем',
        help_text="Толық дұрыс сөйлем, мысалы: 'Сәлем Димаш, Сәлем Джейк'"
    )

    options = models.JSONField(
        verbose_name='Қолжетімді сөздер/сөз тіркестері',
        help_text="Қолданушы таңдауы керек сөздер тізімі, мысалы: ['Димаш', 'Джейк']"
    )

    def __str__(self):
        return f"SelectInsert for Question #{self.question.id}"

    class Meta:
        verbose_name_plural = "Reading | Select Insert"

