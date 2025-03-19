from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users import models as user_models


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Курс атауы"))
    duration = models.PositiveIntegerField(verbose_name=_("Курс ұзақтығы"))
    description = models.CharField(verbose_name=_("Курс түсініктемесі"), null=True, blank=True)
    for_level = models.CharField(verbose_name=_("Қандай левелге арналған"))
    has_level_define = models.BooleanField(default=False, verbose_name=_("Деңгей анықтау барма"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Курс")
        verbose_plural_name = _("Курстар")