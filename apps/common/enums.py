from django.db import models
from django.utils.translation import gettext_lazy as _


class SectionType(models.TextChoices):
    READING = "Reading" ,_("Reading")
    WRITING = "Writing", _("Writing")
    LISTING = "Listing", _("Listing")
    SPEAKING = "Speaking", _("Speaking")

class QuestionType(models.TextChoices):
    SINGLE_CHOICE = "SINGLE_CHOICE", _("Single choice")
    TEXT_ANSWER = "TEXT_ANSWER", _("Text answer")