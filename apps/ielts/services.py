import logging
from typing import List

from rest_framework.exceptions import ValidationError

from apps.common import enums
from apps.ielts.entity_models.ielts_speaking_question import IeltsSpeakingQuestion
from apps.ielts.entity_models.ielts_test import IeltsTest
from apps.ielts.entity_models.ielts_test_submit import IeltsTestSubmit
from apps.llms import openai_cli
from apps.llms.tasks import parse_json_response

logger = logging.getLogger(__name__)


class IeltsSubmitService:
    MAX_ATTEMPTS = 3

    SPEAKING_EVAL_PROMPT = """
You are a certified IELTS Speaking examiner.  
Evaluate the candidate’s answers strictly according to the four official IELTS Speaking criteria
(Fluency & Coherence, Lexical Resource, Grammatical Range Accuracy, Pronunciation).

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

    def speaking_submit(self, test_id: int, data: dict, user) -> float | None:
        """
        Сохраняет speaking‑ответы и получает оценку от LLM.
        Ожидаемый `data`:
        {
          "speakings": [
            {"speaking_id": 11, "answer": "..."},
            ...
          ]
        }
        """
        db_test = IeltsTest.objects.filter(pk=test_id).first()
        if not db_test:
            raise ValidationError("Test not found.")

        speakings = data.get("speakings", [])
        if not speakings:
            raise ValidationError("Speakings list is empty.")

        payload_parts: List[str] = []
        for item in speakings:
            answer = (item.get("answer") or "").strip()
            speaking_id = item.get("speaking_id")
            db_sp = IeltsSpeakingQuestion.objects.filter(pk=speaking_id).first()
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
                score_raw = parsed.get("score")
                if score_raw is not None:
                    final_score = float(score_raw)
                    break
            except Exception:
                logger.exception("LLM evaluation failed – retrying.")

        IeltsTestSubmit.objects.create(
            test=db_test,
            section=enums.ModuleSectionType.SPEAKING,
            user=user,
            score=final_score,
        )
        return final_score
