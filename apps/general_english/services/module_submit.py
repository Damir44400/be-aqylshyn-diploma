import logging
from typing import Dict, Any, Optional, Union

import nltk
from rest_framework.exceptions import ValidationError

from apps.common import enums as common_enums
from apps.general_english import models as general_english_models
from apps.general_english import serializers as general_english_serializers
from apps.llms import openai_cli
from apps.llms.prompts.essay_checker_prompt import get_essay_checker_prompt
from apps.llms.tasks import parse_json_response

logger = logging.getLogger(__name__)


class ModuleSubmitService:
    def _get_module_questions(self, module_id: int, section: str) -> Optional[Any]:
        if section == common_enums.ModuleSectionType.READING:
            return general_english_models.ReadingQuestion.objects.filter(module_id=module_id)
        elif section == common_enums.ModuleSectionType.LISTENING:
            return general_english_models.ListeningQuestion.objects.filter(module_id=module_id)
        return None

    def _calculate_speaking_score(self, context: str, text: str, max_score: float = 1.0,
                                  tolerance: float = 0.5) -> float:
        if not context or not text:
            return 0.0

        distance = nltk.edit_distance(context.strip().lower(), text.strip().lower())
        max_length = max(len(context), len(text))
        if max_length == 0:
            return max_score

        error_rate = distance / max_length
        return max_score if error_rate <= tolerance else 0.0

    def submit_option_answers(self, data: Dict[str, Any], module_id: int) -> float:
        score = 0
        section = data['section_name']

        general_english_models.ModuleScore.objects.filter(
            module_id=module_id, section=section
        ).delete()

        module_questions = self._get_module_questions(module_id, section)
        if not module_questions:
            raise ValidationError(f"No module questions found for section {section}")
        attempts = []
        for option in data.get('options', []):
            question_id = option.get('question_id')
            option_id = option.get('option_id')

            question = (
                module_questions
                .filter(id=question_id)
                .prefetch_related('options')
                .first()
            )
            if not question:
                logger.warning(f"Question {question_id} not found for module {module_id}")
                continue

            correct_option = question.options.filter(is_correct=True).first()
            if correct_option and correct_option.id == option_id:
                score += 1
            attempts.append(
                (
                    option_id,
                    question_id
                )
            )

        module_score = general_english_models.ModuleScore.objects.create(
            module_id=module_id,
            section=section,
            score=score,
        )
        (
            general_english_models
            .OptionAttempt.objects.bulk_create(
                [
                    general_english_models
                    .OptionAttempt(
                        option_id=attempt[0],
                        question_id=attempt[1],
                        module_score=module_score
                    ) for attempt in attempts
                ]
            )
        )
        return score

    def submit_speaking_answers(self, data: Dict[str, Any], module_id: int) -> float:
        score = 0
        section = data['section_name']

        general_english_models.ModuleScore.objects.filter(
            module_id=module_id, section=section
        ).delete()

        db_speakings = general_english_models.Speaking.objects.filter(module_id=module_id)
        if not db_speakings.exists():
            raise ValidationError("No speaking exercises found for this module")

        for answer in data.get("answers", []):
            speaking_id = answer.get('speaking_id')
            text = answer.get('text', '')

            speaking = db_speakings.filter(id=speaking_id).first()
            if not speaking:
                logger.warning(f"Speaking {speaking_id} not found for module {module_id}")
                continue

            score += self._calculate_speaking_score(speaking.context, text)

        general_english_models.ModuleScore.objects.create(
            module_id=module_id,
            section=section,
            score=score,
        )
        return score

    def submit_writing_answers(self, data: Dict[str, Any], module_id: int) -> Union[float, None]:
        section = data['section_name']

        general_english_models.ModuleScore.objects.filter(
            module_id=module_id, section=section
        ).delete()

        writing_data = data.get("writing")
        print(writing_data)
        if not writing_data:
            raise ValidationError("No writing submission provided")

        writing = general_english_models.Writing.objects.filter(module_id=module_id).first()
        print(writing)
        if not writing:
            raise ValidationError("No writing exercise found for this module")

        prompt = get_essay_checker_prompt()
        evaluation_data = {
            "requirements": writing.requirements,
            "user_answer": writing_data
        }

        max_attempts = 3
        final_score = None

        for attempt in range(max_attempts):
            try:
                logger.info(f"Writing evaluation attempt {attempt + 1}/{max_attempts}")

                openai_client = openai_cli.OpenAICLI()
                response = openai_client.send_request(
                    system_prompt=prompt,
                    data=f"requirements: {evaluation_data['requirements']}\nuser answer: {evaluation_data['user_answer']}"
                )

                response_text = response.text if hasattr(response, 'text') else response

                parsed_response = parse_json_response(response_text)
                score = parsed_response.get('writing').get('score')
                if score is not None:
                    try:
                        final_score = float(score)
                        logger.info(f"Successfully evaluated writing: score={final_score}")
                        break
                    except (ValueError, TypeError):
                        logger.warning(f"Received invalid score format: {score}")
                else:
                    logger.warning("No score found in parsed response")

            except Exception as e:
                logger.error(f"Error during writing evaluation: {str(e)}")

        if final_score is None:
            raise ValidationError("Failed to evaluate writing submission after multiple attempts")

        module_score = general_english_models.ModuleScore.objects.create(
            module_id=module_id,
            section=section,
            score=final_score,
        )
        (
            general_english_models
            .WritingAttempt.objects.create(
                writing=writing_data,
                module_score=module_score,
                ai_response=parsed_response.get('improvements'),
            )
        )

        return final_score

    from rest_framework.request import Request
    from typing import Dict, Any

    def get_score(self, request: Request, module_id: int) -> Dict[str, Any]:
        section_name = request.query_params.get('section_name')
        if not section_name:
            raise ValidationError("No section_name query parameter provided")

        module = general_english_models.Module.objects.filter(id=module_id).first()
        if not module:
            raise ValidationError(f"Module with ID {module_id} not found")

        module_section_score = general_english_models.ModuleScore.objects.filter(
            module_id=module_id, section=section_name
        ).first()

        if not module_section_score:
            raise ValidationError(f"No score found for section '{section_name}'")

        payload = {
            "section": section_name,
            "score": module_section_score.score,
        }

        if section_name == "WRITING":
            writing_attempt = general_english_models.WritingAttempt.objects.filter(
                module_score=module_section_score
            ).first()

            if writing_attempt:
                payload["writing"] = {
                    "user_text": writing_attempt.writing,
                    "ai_feedback": writing_attempt.ai_response,
                }

        elif section_name in ["READING", "LISTENING"]:
            test = []
            if section_name == "READING":
                questions = general_english_models.ReadingQuestion.objects.filter(module=module)
                question_serializer_class = general_english_serializers.ReadingQuestionSerializer
            else:
                questions = general_english_models.ListeningQuestion.objects.filter(module=module)
                question_serializer_class = general_english_serializers.ListeningQuestionSerializer

            for question in questions:
                q_data = question_serializer_class(question).data

                options = []
                user_chosen_option = general_english_models.OptionAttempt.objects.filter(
                    question_id=question.pk,
                    module_score=module_section_score
                ).first()

                for option in question.options.all():
                    options.append({
                        "option": option.option,
                        "is_correct": option.is_correct,
                        "is_chosen": user_chosen_option and option.pk == user_chosen_option.option_id,
                    })

                q_data["options"] = options
                test.append(q_data)

            payload["test"] = test

        return payload
