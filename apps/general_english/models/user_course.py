from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.general_english import models as general_english_models
from apps.users import models as user_models


class UserCourse(models.Model):
    course = models.ForeignKey(
        general_english_models.Course,
        on_delete=models.CASCADE,
        verbose_name=_("Қай курсқа тіркелген"),
        related_name="user_courses",
    )
    user = models.ForeignKey(
        user_models.User,
        on_delete=models.CASCADE,
        verbose_name=_("Тіркелген қолданушы")
    )
    user_level = models.CharField(verbose_name=_("Қолданушының деңгейі"))
    last_module = models.ForeignKey(
        general_english_models.Module,
        on_delete=models.CASCADE,
        verbose_name=_("Тоқтаған модуль")
    )

    class Meta:
        unique_together = ("course", "user")

    @property
    def get_progress(self):
        modules = self.user_modules.all()
        total_count = modules.count()
        completed_count = modules.filter(is_completed=True).count()
        return completed_count / total_count * 100

    @property
    def get_modules_count(self):
        return self.user_modules.count()
