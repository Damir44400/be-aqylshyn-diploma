from django.db import models

from apps.ielts.entity_models.ielts_test import IeltsTest


class IeltsSpeakingQuestion(models.Model):
    question = models.TextField()
    additional_information = models.TextField(null=True, blank=True)

    test = models.ForeignKey(IeltsTest, on_delete=models.CASCADE, related_name='speakings')

    def __str__(self):
        return f"{self.question} {self.test}"

    class Meta:
        verbose_name_plural = "Speaking | Tasks"
