from django.db import models
from django.utils.translation import gettext_lazy as _

from .listening_question import ListeningQuestion


class ListeningOption(models.Model):
    question = models.ForeignKey(
        ListeningQuestion,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name=_("Сұрақ")
    )

    option = models.TextField(
        _("Нұсқа мәтіні"), help_text=_("Бұл жауап нұсқасының мәтіні")
    )

    is_correct = models.BooleanField(default=False)
