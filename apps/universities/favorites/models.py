from django.db import models

from apps.universities.models import University
from apps.users.models import User


# Create your models here.
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

