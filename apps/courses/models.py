from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common import enums


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Курс атауы"))
    duration = models.PositiveIntegerField(verbose_name=_("Курс ұзақтығы"))
    description = models.CharField(verbose_name=_("Курс түсініктемесі"), null=True, blank=True)
    has_level_define = models.BooleanField(default=False, verbose_name=_("Деңгей анықтау барма"))
    type = models.CharField(choices=enums.CourseType.choices, default=enums.CourseType.GENERAL_ENGLISH)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Курс")
        verbose_name_plural = _("Курстар")
