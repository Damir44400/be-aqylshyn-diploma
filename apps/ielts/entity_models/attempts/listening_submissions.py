from django.db import models

from apps.common.models import BaseModel
from apps.ielts.entity_models.attempts.ielts_test_attempt import IeltsTestAttempt
from apps.ielts.entity_models.listenings.listening_options import IeltsListeningOption
from apps.ielts.entity_models.listenings.listening_question import IeltsListeningQuestion


class IeltsListeningSubmission(BaseModel):
    attempt = models.ForeignKey(
        IeltsTestAttempt,
        on_delete=models.CASCADE,
        related_name='listening_submissions',
        verbose_name='Test Attempt'
    )
    question = models.ForeignKey(
        IeltsListeningQuestion,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    selected_option = models.ForeignKey(
        IeltsListeningOption,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='Selected Option'
    )
    fill_blank_answer = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Fill-in-the-blanks Answer',
        help_text="Array of candidate answers if the question is fill in the blanks"
    )

    def __str__(self):
        return f"Listening Submission for Q#{self.question.id} by {self.attempt.user}"

    class Meta:
        verbose_name = "IELTS Listening Submission"
        verbose_name_plural = "IELTS Listening Submissions"
