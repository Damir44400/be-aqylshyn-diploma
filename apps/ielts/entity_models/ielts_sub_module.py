from django.db import models

from apps.common import enums
from .ielts_module import IeltsModule


class IeltsSubModule(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Оқу секциясының атауы'
    )
    difficulty = models.CharField(
        max_length=255,
        choices=enums.DifficultyType.choices,
        default=enums.DifficultyType.EASY,
        verbose_name='Қиындық дәрежесі'
    )
    module = models.ForeignKey(
        IeltsModule,
        on_delete=models.CASCADE,
        related_name='sub_modules',
        verbose_name='IELTS модулі'
    )

    class Meta:
        verbose_name = 'Оқу тапсырмасы'
        verbose_name_plural = 'Оқу тапсырмалары'

    def __str__(self):
        return f"{self.title} - {self.get_difficulty_display()}"
