from django.db import models
from django.utils.translation import gettext_lazy as _

from .module import Module


class Writing(models.Model):
    title = models.TextField(_("Оқу мазмүны"), help_text=_("Бұл сұрақ қатысты мәтін үзіндісі"))
    requirements = models.TextField(_("Тема түсініктемесі"),
                                    help_text=_("Бұл түсініктеме қолданшыны тексергенде қаралатын анықтама секілді"))
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        verbose_name=_("Қай модульге тиесілі"),
        related_name="writing",
    )
