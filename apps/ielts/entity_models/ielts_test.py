from django.db import models

from .ielts_sub_module import IeltsSubModule


class IeltsTest(models.Model):
    name = models.CharField(max_length=100)
    sub_model = models.ForeignKey(IeltsSubModule, on_delete=models.CASCADE, related_name='tests')

    class Meta:
        verbose_name_plural = "Admin | IELTS Tests"

    def __str__(self):
        return self.name