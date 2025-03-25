from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.common import enums
from apps.general_english import models


@receiver(post_save, sender=models.ModuleScore)
def check_module_completion(sender, instance, created, **kwargs):
    writing_completed = False
    reading_completed = False
    speaking_completed = False
    listening_completed = False

    module = instance.module

    writing_section = models.ModuleScore.objects.filter(
        section=enums.ModuleSectionType.WRITING,
        module=instance.module
    )
    if writing_section.exists():
        writing_completed = True

    reading_section = models.ModuleScore.objects.filter(
        section=enums.ModuleSectionType.READING,
        module=instance.module
    )
    if reading_section.exists():
        reading_completed = True

    speaking_section = models.ModuleScore.objects.filter(
        section=enums.ModuleSectionType.SPEAKING,
        module=instance.module
    )
    if speaking_section.exists():
        speaking_completed = True

    listening_section = models.ModuleScore.objects.filter(
        section=enums.ModuleSectionType.LISTENING,
        module=instance.module
    )
    if listening_section.exists():
        listening_completed = True

    if writing_completed and reading_completed and speaking_completed and listening_completed:
        module.is_completed = True
        module.save()

    user_progress = models.UserProgress.objects.filter(
        user=module.user_course.user,
    ).first()

    user_progress.last_module = module
    user_progress.save()