from django.db import models

from apps.common import enums
from apps.users import models as user_models


class IeltsSubmit(models.Model):
    instance_id = models.IntegerField()
    section = models.CharField(choices=enums.ModuleSectionType)

    user_id = models.ForeignKey(user_models.User, on_delete=models.CASCADE)

    score = models.IntegerField()

    submitted_at = models.DateTimeField(auto_now_add=True)
