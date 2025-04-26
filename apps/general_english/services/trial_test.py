from rest_framework.exceptions import ValidationError

from apps.common import enums as common_enums
from apps.courses import models as course_models
from apps.general_english import models as general_english_models
from apps.llms.tasks.generate_modules import generate_modules


class TrialTestService:
    @staticmethod
    def trial_test_answer_check(course_id, data, user):
        score = 0

        user_progresses = general_english_models.UserProgress.objects.filter(
            user=user, course_id=course_id
        )
        if user_progresses:
            user_progresses.delete()

        course = course_models.Course.objects.filter(id=course_id).first()
        if not course:
            raise ValidationError({"detail": "Course not found"})

        trial_questions = general_english_models.TrialQuestion.objects.filter(course_id=course_id)
        if not trial_questions.exists():
            raise ValidationError({"detail": 'No trial questions found for this course'})

        question_map = {q.id: q for q in trial_questions}

        user_answers_log = ""

        for answer in data.get('answers', []):
            question_id = answer.get('question_id')
            selected_option_id = answer.get('option_id')

            question = question_map.get(question_id)
            if not question or not selected_option_id:
                continue

            selected_option = question.trial_options.filter(id=selected_option_id).first()
            if not selected_option:
                continue

            correct_option = question.trial_options.filter(is_correct=True).first()

            if (
                    question.question_type == common_enums.QuestionType.SINGLE_CHOICE
                    and correct_option and correct_option.id == selected_option_id
            ):
                score += 1

            user_answers_log += (
                f"{question_id}. Question: {question.question}\n"
                f"User Answer: {selected_option.option}\n"
            )
            if correct_option:
                user_answers_log += f"Correct Answer: {correct_option.option}\n" if question.question_type == common_enums.QuestionType.SINGLE_CHOICE else ""

        user_answers_log += f"\n\n\nUser scored in test quizzes: {score}"

        user_progress = general_english_models.UserProgress.objects.create(
            user=user,
            course_id=course_id,
            score=score
        )

        generate_modules.apply_async(
            kwargs={"user": user, "user_course_id": user_progress.pk, "score": score,
                    "user_answers_log": user_answers_log})
        if score >= 8:
            user_level = "Advanced"  # C1-C2
        elif score >= 5:
            user_level = "Intermediate"  # B1-B2
        else:
            user_level = "Beginner"  # A1-A2

        return score, user_level
