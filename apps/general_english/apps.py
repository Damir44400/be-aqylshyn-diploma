from django.apps import AppConfig


class GeneralEnglishConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.general_english'
    verbose_name = 'General English'

    def ready(self):
        from apps.general_english import signals
