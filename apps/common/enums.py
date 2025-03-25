from django.db import models
from django.utils.translation import gettext_lazy as _


class QuestionType(models.TextChoices):
    SINGLE_CHOICE = "SINGLE_CHOICE", _("Single choice")
    TEXT_ANSWER = "TEXT_ANSWER", _("Text answer")


class CourseType(models.TextChoices):
    IELTS = "IELTS", _("IELTS")
    GENERAL_ENGLISH = "GENERAL ENGLISH", _("General English")


class ModuleSectionType(models.TextChoices):
    READING = "READING", _("Reading")
    WRITING = "WRITING", _("Writing")
    LISTENING = "LISTENING", _("LISTENING")
    SPEAKING = "SPEAKING", _("Speaking")
