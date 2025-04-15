from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.ielts.entity_models.ielts_test import IeltsTest


class IeltsTestAttempt(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ielts_attempts',
        verbose_name='Candidate'
    )
    test = models.ForeignKey(
        IeltsTest,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='IELTS Test'
    )
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='Start Time')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Completion Time')

    def __str__(self):
        return f"Attempt by {self.user} for {self.test}"

    class Meta:
        verbose_name = "IELTS Test Attempt"
        verbose_name_plural = "IELTS Test Attempts"
