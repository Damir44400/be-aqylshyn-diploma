from django.db import models
from django.utils.translation import gettext_lazy as _

from .reading_question import ReadingQuestion


class ReadingOption(models.Model):
    question = models.ForeignKey(
        ReadingQuestion,
        on_delete=models.CASCADE,
        related_name='reading_options',
        verbose_name=_("Сұрақ")
    )
    option = models.TextField(
        _("Нұсқа мәтіні"), help_text=_("Бұл жауап нұсқасының мәтіні")
    )
    is_correct = models.BooleanField(
        _("Дұрыс па"), default=False,
        help_text=_("Бұл нұсқа дұрыс жауап болып табылады ма")
    )
