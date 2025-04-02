from django.db import models

from ..ielts_test import IeltsTest


class IeltsListening(models.Model):
    title = models.CharField()
    audio_file = models.FileField()
    test = models.ForeignKey(IeltsTest, on_delete=models.CASCADE, related_name='listenings')

    def __str__(self):
        return self.title
