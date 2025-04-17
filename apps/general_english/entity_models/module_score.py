from django.db import models

from apps.common import enums
from apps.general_english import models as general_english_models


class ModuleScore(models.Model):
    module = models.ForeignKey(general_english_models.Module, on_delete=models.CASCADE)
    section = models.CharField(choices=enums.ModuleSectionType.choices, max_length=10)
    score = models.FloatField(default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class OptionAttempt(models.Model):
    module_score = models.ForeignKey(ModuleScore, on_delete=models.CASCADE, related_name='option_attempts')
    option_id = models.IntegerField()
    question_id = models.IntegerField(null=True)


class WritingAttempt(models.Model):
    module_score = models.ForeignKey(ModuleScore, on_delete=models.CASCADE, related_name='writing_attempts')
    writing = models.TextField()
    ai_response = models.TextField()
