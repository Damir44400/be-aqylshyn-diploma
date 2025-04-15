from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.ielts.entity_models.attempts.ielts_test_attempt import IeltsTestAttempt
from apps.ielts.entity_models.attempts.listening_submissions import IeltsListeningSubmission
from apps.ielts.entity_models.attempts.reading_submissions import IeltsReadingSubmission
from apps.ielts.entity_models.attempts.writing_submissions import IeltsWritingSubmission
from apps.ielts.entity_models.ielts_test import IeltsTest
from apps.ielts.entity_models.ielts_writing import IeltsWriting
from apps.ielts.entity_models.listenings.listening_options import IeltsListeningOption
from apps.ielts.entity_models.listenings.listening_question import IeltsListeningQuestion
from apps.ielts.entity_models.readings.reading_options import IeltsReadingOption
from apps.ielts.entity_models.readings.reading_question import IeltsReadingQuestion


class IeltsTestService:
    def create_test_attempt(self, test_id, user):
        test = IeltsTest.objects.filter(id=test_id).first()
        if test is None:
            raise ValidationError({"detail": "Test not found"})
        attempt = IeltsTestAttempt.objects.create(user=user, test=test)
        return attempt

    def complete_test_attempt(self, attempt_id, user):
        attempt = IeltsTestAttempt.objects.filter(id=attempt_id, user=user).first()
        if attempt is None:
            raise ValidationError({"detail": "Attempt not found"})
        attempt.completed_at = timezone.now()
        attempt.save()
        return attempt

    def submit_reading_answer(self, attempt_id, question_id, data, user):
        attempt = IeltsTestAttempt.objects.filter(id=attempt_id, user=user).first()
        if attempt is None:
            raise ValidationError({"detail": "Attempt not found"})

        question = IeltsReadingQuestion.objects.filter(id=question_id).first()
        if question is None:
            raise ValidationError({"detail": "Reading question not found"})

        selected_option_id = data.get('selected_option')
        fill_blank_answer = data.get('fill_blank_answer')
        select_insert_answer = data.get('select_insert_answer')

        option_instance = None
        if selected_option_id:
            option_instance = IeltsReadingOption.objects.filter(id=selected_option_id).first()
            if option_instance is None:
                raise ValidationError({"detail": "Option not found"})

        submission = IeltsReadingSubmission.objects.create(
            attempt=attempt,
            question=question,
            selected_option=option_instance,
            fill_blank_answer=fill_blank_answer,
            select_insert_answer=select_insert_answer
        )
        return submission

    def submit_listening_answer(self, attempt_id, question_id, data, user):
        attempt = IeltsTestAttempt.objects.filter(id=attempt_id, user=user).first()
        if attempt is None:
            raise ValidationError({"detail": "Attempt not found"})

        question = IeltsListeningQuestion.objects.filter(id=question_id).first()
        if question is None:
            raise ValidationError({"detail": "Listening question not found"})

        selected_option_id = data.get('selected_option')
        fill_blank_answer = data.get('fill_blank_answer')

        option_instance = None
        if selected_option_id:
            option_instance = IeltsListeningOption.objects.filter(id=selected_option_id).first()
            if option_instance is None:
                raise ValidationError({"detail": "Option not found"})

        submission = IeltsListeningSubmission.objects.create(
            attempt=attempt,
            question=question,
            selected_option=option_instance,
            fill_blank_answer=fill_blank_answer
        )
        return submission

    def submit_writing_answer(self, attempt_id, writing_id, data, user):
        attempt = IeltsTestAttempt.objects.filter(id=attempt_id, user=user).first()
        if attempt is None:
            raise ValidationError({"detail": "Attempt not found"})

        writing = IeltsWriting.objects.filter(id=writing_id).first()
        if writing is None:
            raise ValidationError({"detail": "Writing task not found"})

        answer_text = data.get('answer_text')
        if not answer_text:
            raise ValidationError({"detail": "Answer text is required"})

        submission = IeltsWritingSubmission.objects.create(
            attempt=attempt,
            writing=writing,
            answer_text=answer_text
        )
        return submission
