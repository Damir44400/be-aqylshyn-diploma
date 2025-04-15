from django.db import models

from apps.common import models as common_models


class IeltsModule(common_models.BaseModel, models.Model):
    cover = models.ImageField(
        upload_to='ielts/modules/',
        verbose_name='Модульдің суреті'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Модульдің атауы'
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )

    class Meta:
        verbose_name_plural = "Admin | IELTS Modules"

    def __str__(self):
        return self.title
