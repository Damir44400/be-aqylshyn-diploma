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


class DifficultyType(models.TextChoices):
    EASY = "EASY", _("Easy")
    MEDIUM = "MEDIUM", _("Medium")
    HARD = "HARD", _("Hard")


class IeltsReadingQuestionType(models.TextChoices):
    FILL_BLANK = 'FILL', _('Fill in the Blank')
    SELECT_INSERT = 'SELECT_INSERT', _('Select and place in correct order')
    OPTIONS = 'OPTIONS', _('Choice Options')


class IeltsListeningQuestionType(models.TextChoices):
    FILL_BLANK = 'FILL', _('Fill in the Blank')
    OPTIONS = 'OPTIONS', _('Choice Options')

class ChatSenderType(models.TextChoices):
    USER = "USER", _("User")
    AI = "AI", _("AI")


class IeltsWritingPart(models.IntegerChoices):
    PART1 = 1, "Part 1"
    PART2 = 2, "Part 2"

class IELTSSpeakingPart(models.IntegerChoices):
    PART1 = 1, "Part 1 (Interview)"
    PART2 = 2, "Part 2 (Long Turn / Cue Card)"
    PART3 = 3, "Part 3 (Discussion)"

class IELTSListeningPart(models.IntegerChoices):
    PART1 = 1, "Part 1"
    PART2 = 2, "Part 2"
    PART3 = 3, "Part 3"
    PART4 = 4, "Part 4"

class IELTSReadingPassage(models.IntegerChoices):
    PASSAGE_1 = 1, "Passage 1"
    PASSAGE_2 = 2, "Passage 2"
    PASSAGE_3 = 3, "Passage 3"