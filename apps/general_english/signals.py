from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.common import enums
from apps.general_english import models


@receiver(post_save, sender=models.ModuleScore)
def check_module_completion(sender, instance, created, **kwargs):
    module = instance.module

    completed_sections = models.ModuleScore.objects.filter(
        module=module
    ).values_list('section', flat=True)

    required_sections = {
        enums.ModuleSectionType.WRITING,
        enums.ModuleSectionType.READING,
        enums.ModuleSectionType.SPEAKING,
        enums.ModuleSectionType.LISTENING,
    }

    if required_sections.issubset(set(completed_sections)):
        module.is_completed = True
        module.save()

    user_progress = models.UserProgress.objects.filter(
        user=module.user_course.user
    ).first()

    if user_progress:
        user_progress.last_module = module
        user_progress.save()
