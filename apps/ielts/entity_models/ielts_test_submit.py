from django.db import models

from apps.common import enums
from apps.ielts.entity_models.ielts_test import IeltsTest
from apps.users import models as user_models


class IeltsTestSubmit(models.Model):
    test = models.ForeignKey(IeltsTest, on_delete=models.CASCADE)
    section = models.CharField(choices=enums.ModuleSectionType.choices)

    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)

    score = models.FloatField()

    submitted_at = models.DateTimeField(auto_now_add=True)
