from django.db import models

from apps.ielts.entity_models.ielts_writing import IeltsWriting
from apps.users.models import User


class IeltsWritingSubmission(models.Model):
    writing = models.ForeignKey(IeltsWriting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    user_answer = models.TextField(blank=True, null=True)
    exception_corrections = models.TextField(blank=True, null=True)

    score = models.FloatField(blank=True, null=True)
