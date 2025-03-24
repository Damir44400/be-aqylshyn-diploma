from django.db import models
from django.utils.translation import gettext_lazy as _


class Module(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Модуль атауы"))
    is_completed = models.BooleanField(default=False, verbose_name=_("Модуль аяқталыдма?"))
    user_course = models.ForeignKey(
        "general_english.UserProgress",
        on_delete=models.CASCADE,
        verbose_name=_("Қолданушы курсы"),
        related_name="user_modules",
    )
    improvement = models.TextField(verbose_name=_("Қолданушыға бағытталған күшейтулер"))

    has_writing = models.BooleanField(default=True)
    has_reading = models.BooleanField(default=True)
    has_listening = models.BooleanField(default=True)
    has_speaking = models.BooleanField(default=True)

    def __str__(self):
        return f"Модуль №{self.pk} {self.name}"
