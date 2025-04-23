from django.db import models

from apps.ielts import models as ielts_models


class IeltsListening(models.Model):
    title = models.CharField(max_length=255)
    audio_file = models.FileField()
    test = models.OneToOneField(ielts_models.IeltsTest, on_delete=models.CASCADE, related_name='listening')

    def __str__(self):
        return f"{self.title} {self.test}"

    class Meta:
        verbose_name_plural = "Listening | Audio File"
