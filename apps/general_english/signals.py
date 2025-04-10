from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.common import enums
from apps.general_english import models


@receiver(post_save, sender=models.ModuleScore)
def check_module_completion(sender, instance, created, **kwargs):
    module = instance.module
    print(f"Signal triggered for ModuleScore {instance.id} of module {module.id}")

    completed_sections = set(models.ModuleScore.objects.filter(
        module=module
    ).values_list('section', flat=True).distinct())

    required_sections = {
        enums.ModuleSectionType.WRITING,
        enums.ModuleSectionType.READING,
        enums.ModuleSectionType.SPEAKING,
        enums.ModuleSectionType.LISTENING,
    }

    print(f"Completed: {completed_sections}")
    print(f"Required: {required_sections}")

    is_complete = required_sections.issubset(completed_sections)
    print(f"Module complete: {is_complete}")

    try:
        user_progress = models.UserProgress.objects.get(
            user=module.user_course.user
        )

        if is_complete != module.is_completed:
            module.is_completed = is_complete
            module.save(update_fields=['is_completed'])
            print(f"Updated module {module.id} completion to {is_complete}")

        if is_complete:
            next_module = models.Module.objects.filter(
                user_course=module.user_course,
                id__gt=module.id
            ).order_by('id').first()

            if next_module:
                if user_progress.last_module != next_module:
                    user_progress.last_module = next_module
                    user_progress.save(update_fields=['last_module'])
                    print(f"Updated last module to next module {next_module.id} for user {module.user_course.user.id}")
            else:
                print(f"No next module found after module {module.id} for user {module.user_course.user.id}")

    except models.UserProgress.DoesNotExist:
        print(f"No UserProgress found for user {module.user_course.user.id}")
