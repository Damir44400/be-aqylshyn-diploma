from django.db import models
from django.utils.translation import gettext_lazy as _

from ..module import Module


class ListeningQuestion(models.Model):
    audio_question = models.FileField(verbose_name=_("Аудио сұрақ"))
    context = models.CharField(verbose_name=_("Аудио сұрақ тексті"))

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="listening_questions")