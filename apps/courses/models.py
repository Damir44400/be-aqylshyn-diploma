from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Курстың атауы"))
    level_define = models.BooleanField(default=True, verbose_name=_("Деңгей анықтау"))
    duration = models.FloatField(verbose_name=_("Өту уақыты"))

    @property
    def modules_count(self):
        return self.modules.all().count()


class Module(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Модуль атауы"))
    course = models.ForeignKey(
        Course,
        related_name='modules',
        on_delete=models.CASCADE,
        verbose_name=_("Қай курсқа тиесілі")
    )
    order = models.IntegerField(verbose_name=_("Модульдың қатары"))
