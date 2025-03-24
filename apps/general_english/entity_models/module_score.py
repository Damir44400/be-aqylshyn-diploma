from django.db import models

from apps.common import enums
from apps.general_english import models as general_english_models
from apps.users import models as user_models


class ModuleScore(models.Model):
    module = models.ForeignKey(general_english_models.Module, on_delete=models.CASCADE)
    section = models.CharField(choices=enums.ModuleSectionType, max_length=10)
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    score = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)