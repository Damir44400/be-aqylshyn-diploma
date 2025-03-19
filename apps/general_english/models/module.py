from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.general_english import models as general_english_models


class Module(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Модуль атауы"))
    order = models.PositiveIntegerField(verbose_name=_("Модуль қатары"))
    is_completed = models.BooleanField(default=False, verbose_name=_("Модуль аяқталыдма?"))
    user_course = models.ForeignKey(
        general_english_models.UserCourse,
        on_delete=models.CASCADE,
        verbose_name=_("Қолданушы курсы"),
        related_name="user_modules",
    )

    def __str__(self):
        return f"{self.order}. Модуль №{self.pk} {self.name}"
