import logging
from typing import List

from rest_framework.exceptions import ValidationError

from apps.common import enums
from apps.ielts.entity_models.ielts_test import IeltsTest
from apps.ielts.entity_models.ielts_test_submit import IeltsTestSubmit
from apps.ielts.entity_models.ielts_writing import IeltsWriting
from apps.ielts.entity_models.listenings.listening import IeltsListening
from apps.ielts.entity_models.listenings.listening_options import IeltsListeningFillBlank, IeltsListeningOption
from apps.ielts.entity_models.listenings.listening_question import IeltsListeningQuestion
from apps.ielts.entity_models.readings.reading import IeltsReading
from apps.ielts.entity_models.readings.reading_options import IeltsReadingOption, IeltsReadingFillBlank, \
    IeltsReadingSelectInsert
from apps.ielts.entity_models.readings.reading_question import IeltsReadingQuestion
from apps.ielts.entity_models.speakings.speaking_parts import IeltsSpeakingPart
from apps.ielts.entity_models.speakings.speaking_questions import IeltsSpeakingQuestion
from apps.llms import openai_cli
from apps.llms.tasks import parse_json_response

logger = logging.getLogger(__name__)


class IeltsSubmitService:
    MAX_ATTEMPTS = 3

    WRITING_EVAL_PROMPT = """
You are a certified IELTS Writing examiner.
Evaluate the candidate’s responses strictly according to the four official IELTS Writing criteria
(Task Achievement, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy).

OUTPUT FORMAT – return **only** valid JSON:

{
  "score": 0.0‑9.0 (float, one decimal place),
  "breakdown": {
    "task_achievement": 0‑9 (float),
    "coherence_and_cohesion": 0‑9 (float),
    "lexical_resource": 0‑9 (float),
    "grammatical_range_and_accuracy": 0‑9 (float)
  },
  "feedback": "Concise, actionable advice (max 120 words)"
}

IMPORTANT:
- Round band scores to the nearest .0 or .5.
- Score **only** on what the candidate actually writes; do not invent content.
- The JSON **must** parse without errors – no extra keys, comments or trailing commas.
"""

    SPEAKING_EVAL_PROMPT = """
You are a certified IELTS Speaking examiner.
Evaluate the candidate’s answers strictly according to the four official IELTS Speaking criteria
(Fluency & Coherence, Lexical Resource, Grammatical Range & Accuracy, Pronunciation).

OUTPUT FORMAT – return **only** valid JSON:

{
  "score": 5.0‑9.0 (float, one decimal place),
  "breakdown": {
    "fluency_and_coherence": 0‑9 (float),
    "lexical_resource": 0‑9 (float),
    "grammatical_range_and_accuracy": 0‑9 (float),
    "pronunciation": 0‑9 (float)
  },
  "feedback": "Concise, actionable advice (max 120 words)"
}

IMPORTANT:
- Round band scores to the nearest .0 or .5.
- Score **only** on what the candidate actually says; do not invent content.
- The JSON **must** parse without errors – no extra keys, comments or trailing commas.
"""

    def writing_submit(self, test_id: int, data: dict, user) -> float:
        db_test = IeltsTest.objects.filter(pk=test_id).first()
        if not db_test:
            raise ValidationError("Test not found.")

        IeltsTestSubmit.objects.filter(
            test=db_test,
            section=enums.ModuleSectionType.WRITING,
            user=user
        ).delete()

        writings = data.get("writings", [])
        if not writings:
            raise ValidationError("Writings list is empty.")

        payload_parts: List[str] = []
        for writing in writings:
            answer = (writing.get("answer") or "").strip()
            writing_id = writing.get("writing_id")
            db_writing = IeltsWriting.objects.filter(pk=writing_id, test=db_test).first()
            if not db_writing:
                logger.warning("Writing question %s not found – skipped.", writing_id)
                continue

            payload_parts.append(
                f"Question: {db_writing.context}\nCandidate answer: {answer}\n"
            )

        if not payload_parts:
            raise ValidationError("No valid writing answers provided.")

        prompt_payload = "\n\n".join(payload_parts)

        final_score: float | None = None
        for _ in range(self.MAX_ATTEMPTS):
            try:
                response = openai_cli.OpenAICLI().send_request(
                    system_prompt=self.WRITING_EVAL_PROMPT,
                    data=prompt_payload,
                )
                parsed = parse_json_response(response)
                if "score" in parsed:
                    final_score = float(parsed["score"])
                    break
            except Exception:
                logger.exception("LLM evaluation failed – retrying.")

        if final_score is None:
            raise ValidationError("Failed to get a score from the evaluation model.")

        IeltsTestSubmit.objects.create(
            test=db_test,
            section=enums.ModuleSectionType.WRITING,
            user=user,
            score=final_score,
        )
        return final_score

    def speaking_submit(self, test_id: int, data: dict, user) -> float:
        db_test = IeltsTest.objects.filter(pk=test_id).first()
        if not db_test:
            raise ValidationError("Test not found.")

        IeltsTestSubmit.objects.filter(
            test=db_test,
            section=enums.ModuleSectionType.SPEAKING,
            user=user
        ).delete()

        speakings = data.get("speakings", [])
        if not speakings:
            raise ValidationError("Speakings list is empty.")

        payload_parts: List[str] = []
        for item in speakings:
            answer = (item.get("answer") or "").strip()
            speaking_id = item.get("speaking_id")
            speaking_parts = IeltsSpeakingPart.objects.filter(test=db_test).all()
            for speaking_part in speaking_parts:
                db_sp = IeltsSpeakingQuestion.objects.filter(
                    pk=speaking_id, part=speaking_part
                ).first()
                if not db_sp:
                    logger.warning("Speaking question %s not found – skipped.", speaking_id)
                    continue

                payload_parts.append(
                    f"Question: {db_sp.question}\nCandidate answer: {answer}\n"
                )

        if not payload_parts:
            raise ValidationError("No valid speaking answers provided.")

        prompt_payload = "\n\n".join(payload_parts)

        final_score: float | None = None
        for _ in range(self.MAX_ATTEMPTS):
            try:
                response = openai_cli.OpenAICLI().send_request(
                    system_prompt=self.SPEAKING_EVAL_PROMPT,
                    data=prompt_payload,
                )
                parsed = parse_json_response(response)
                if "score" in parsed:
                    final_score = float(parsed["score"])
                    break
            except Exception:
                logger.exception("LLM evaluation failed – retrying.")

        if final_score is None:
            raise ValidationError("Failed to get a score from the evaluation model.")

        IeltsTestSubmit.objects.create(
            test=db_test,
            section=enums.ModuleSectionType.SPEAKING,
            user=user,
            score=final_score,
        )
        return final_score

    def reading_submit(self, test_id: int, data: dict, user) -> float:
        db_test = IeltsTest.objects.filter(pk=test_id).first()
        if not db_test:
            raise ValidationError("Test not found.")

        IeltsTestSubmit.objects.filter(
            test=db_test,
            section=enums.ModuleSectionType.READING,
            user=user
        ).delete()

        readings = data.get("readings", [])
        if not readings:
            raise ValidationError("Readings list is empty.")

        total_score = 0
        processed = False

        for reading in readings:
            reading_id = reading.get("reading_id")
            db_reading = IeltsReading.objects.filter(
                pk=reading_id,
                test=db_test
            ).first()
            if not db_reading:
                logger.warning("Reading passage %s not found – skipped.", reading_id)
                continue

            processed = True

            for option in reading.get("options", []):
                question_id = option.get("question_id")
                selected_id = option.get("option_id")
                db_question = IeltsReadingQuestion.objects.filter(
                    pk=question_id,
                    reading=db_reading
                ).first()
                if not db_question:
                    logger.warning("Reading question %s not found – skipped.", question_id)
                    continue

                correct = IeltsReadingOption.objects.filter(
                    question=db_question,
                    is_correct=True
                ).values_list("pk", flat=True).first()
                if correct == selected_id:
                    total_score += 1

            for fill in reading.get("fills", []):
                question_id = fill.get("question_id")
                answer = (fill.get("answer") or []).strip()
                db_question = IeltsReadingQuestion.objects.filter(
                    pk=question_id,
                    reading=db_reading
                ).first()
                if not db_question:
                    logger.warning("Fill question %s not found – skipped.", question_id)
                    continue

                correct_answer = IeltsReadingFillBlank.objects.filter(
                    question=db_question
                ).values_list("answer", flat=True).first()
                if correct_answer is not None and correct_answer == answer:
                    total_score += 1

            for select in reading.get("selects", []):
                question_id = select.get("question_id")
                answer = (select.get("answer") or "").strip()
                db_question = IeltsReadingQuestion.objects.filter(
                    pk=question_id,
                    reading=db_reading
                ).first()
                if not db_question:
                    logger.warning("Select question %s not found – skipped.", question_id)
                    continue

                correct_answer = IeltsReadingSelectInsert.objects.filter(
                    question=db_question
                ).values_list("correct_answer", flat=True).first()
                if correct_answer is not None and correct_answer.strip().lower() == answer.lower():
                    total_score += 1

        if not processed:
            raise ValidationError("No valid reading answers provided.")

        IeltsTestSubmit.objects.create(
            test=db_test,
            section=enums.ModuleSectionType.READING,
            user=user,
            score=total_score,
        )
        return total_score

    def listening_submit(self, test_id: int, data: dict, user) -> float:
        db_test = IeltsTest.objects.filter(pk=test_id).first()
        if not db_test:
            raise ValidationError("Test not found.")
        IeltsTestSubmit.objects.filter(
            test=db_test,
            section=enums.ModuleSectionType.LISTENING,
            user=user
        ).delete()

        listening = data.get("listening", {})
        if not listening:
            raise ValidationError("Listenings list is empty.")

        total_score = 0

        listening_id = listening.get("listening_id")
        db_listening = IeltsListening.objects.filter(
            pk=listening_id,
            test=db_test
        ).first()

        processed = True

        for option in listening.get("options", []):
            question_id = option.get("question_id")
            selected_id = option.get("option_id")
            db_question = IeltsListeningQuestion.objects.filter(
                pk=question_id,
                listening=db_listening
            ).first()
            if not db_question:
                logger.warning("Listening question %s not found – skipped.", question_id)
                continue

            correct_pk = IeltsListeningOption.objects.filter(
                question=db_question,
                is_correct=True
            ).values_list("pk", flat=True).first()
            if correct_pk == selected_id:
                total_score += 1

        for fill in listening.get("fills", []):
            question_id = fill.get("question_id")
            answer = (fill.get("answer") or [])
            db_question = IeltsListeningQuestion.objects.filter(
                pk=question_id,
                listening=db_listening
            ).first()
            if not db_question:
                logger.warning("Fill question %s not found – skipped.", question_id)
                continue

            correct_answer = IeltsListeningFillBlank.objects.filter(
                question=db_question
            ).values_list("answer", flat=True).first()
            if correct_answer and correct_answer == answer:
                total_score += 1

        if not processed:
            raise ValidationError("No valid listening answers provided.")

        IeltsTestSubmit.objects.create(
            test=db_test,
            section=enums.ModuleSectionType.LISTENING,
            user=user,
            score=total_score,
        )
        return total_score
