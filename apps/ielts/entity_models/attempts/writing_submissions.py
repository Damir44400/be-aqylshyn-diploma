from django.db import models

from apps.common.models import BaseModel
from apps.ielts.entity_models.attempts.ielts_test_attempt import IeltsTestAttempt
from apps.ielts.entity_models.ielts_writing import IeltsWriting


class IeltsWritingSubmission(BaseModel):
    attempt = models.ForeignKey(
        IeltsTestAttempt,
        on_delete=models.CASCADE,
        related_name='writing_submissions',
        verbose_name='Test Attempt'
    )
    writing = models.ForeignKey(
        IeltsWriting,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Writing Task'
    )
    answer_text = models.TextField(verbose_name="Candidate's Answer")

    def __str__(self):
        return f"Writing Submission for Task Q#{self.writing.id} by {self.attempt.user}"

    class Meta:
        verbose_name = "IELTS Writing Submission"
        verbose_name_plural = "IELTS Writing Submissions"
