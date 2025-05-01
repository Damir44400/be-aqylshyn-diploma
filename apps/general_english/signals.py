from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.common.enums import ModuleSectionType
from apps.general_english import models


@receiver(post_save, sender=models.ModuleScore)
def check_module_completion(sender, instance, created, **kwargs):
    module = instance.module

    def _update_progress():
        completed = set(
            module.modulescore_set
            .values_list('section', flat=True)
            .distinct()
        )

        required = {
            ModuleSectionType.WRITING.value,
            ModuleSectionType.READING.value,
            ModuleSectionType.SPEAKING.value,
            ModuleSectionType.LISTENING.value,
        }

        is_complete = required.issubset(completed)

        if is_complete and not module.is_completed:
            module.is_completed = is_complete
            module.save(update_fields=['is_completed'])

        progress = models.UserProgress.objects.filter(
            course=module.user_course.course
        ).first()
        if is_complete:
            lookup = {
                'user_course': module.user_course,
                'order__gt': module.order,
            }
            next_mod = models.Module.objects.filter(**lookup) \
                .order_by('order') \
                .first()
            if next_mod:
                progress.last_module = next_mod
                progress.save(update_fields=['last_module'])

    transaction.on_commit(_update_progress)
