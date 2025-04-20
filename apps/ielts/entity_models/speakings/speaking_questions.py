from django.db import models

from apps.ielts import models as ielts_models


class IeltsSpeakingQuestion(models.Model):
    question = models.TextField()
    additional_information = models.TextField(null=True, blank=True)
    part = models.ForeignKey(ielts_models.IeltsSpeakingPart, on_delete=models.CASCADE, related_name='speaking_questions')

    def __str__(self):
        return f"{self.question} {self.part}"

    class Meta:
        verbose_name_plural = "Speaking | Tasks"
