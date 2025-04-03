from django.db import models

from apps.users.models import User
from .listening import IeltsListening


class ListeningSubmit(models.Model):
    listening_id = models.ForeignKey(IeltsListening, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
