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
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Қатар',
    )

    class Meta:
        verbose_name_plural = "Admin | IELTS SubModules"

    def __str__(self):
        return f"{self.title} - {self.get_difficulty_display()}"

    def save(self, *args, **kwargs):
        if self._state.adding and self.order == 0:
            last_order = IeltsSubModule.objects.filter(module=self.module).aggregate(models.Max('order'))[
                             'order__max'] or 0
            self.order = last_order + 1
        super().save(*args, **kwargs)
