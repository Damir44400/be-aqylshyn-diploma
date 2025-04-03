from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users import models as user_models


class UserProgress(models.Model):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        verbose_name=_("Қай курсқа тіркелген"),
        related_name="user_course",
    )
    user = models.ForeignKey(
        user_models.User,
        on_delete=models.CASCADE,
        verbose_name=_("Тіркелген қолданушы"),
        related_name="user_progresses",
    )
    score = models.IntegerField(
        default=0,
        validators=[validators.MinValueValidator(0)],
        verbose_name=_("Қолданушының жинаған ұпай саны")
    )
    last_module = models.ForeignKey(
        "general_english.Module",
        on_delete=models.CASCADE,
        verbose_name=_("Тоқтаған модуль"),
        null=True,
    )
    level = models.CharField(
        null=True,
        verbose_name=_("Қолданушы уровеньі"),
    )

    class Meta:
        unique_together = ("course", "user")

    @property
    def get_progress(self):
        modules = self.user_modules.all()
        total_count = modules.count()
        completed_count = modules.filter(is_completed=True).count()
        if completed_count == 0:
            return 0
        return completed_count / total_count * 100

    @property
    def get_modules_count(self):
        return self.user_modules.count()
