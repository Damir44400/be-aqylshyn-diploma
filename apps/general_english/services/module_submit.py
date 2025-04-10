import logging
from typing import Dict, Any, Optional, Union

import nltk
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from apps.common import enums as common_enums
from apps.general_english import models as general_english_models
from apps.llms import openai_cli
from apps.llms.prompts.essay_checker_prompt import get_essay_checker_prompt
from apps.llms.tasks import parse_json_response

logger = logging.getLogger(__name__)


class ModuleSubmitService:
    """Service for handling module submissions across different section types."""

    def _get_module_questions(self, module_id: int, section: str) -> Optional[Any]:
        """
        Retrieve questions for a specific module and section.

        Args:
            module_id: The ID of the module
            section: The section type (reading, listening, etc.)

        Returns:
            QuerySet of questions or None if section not supported
        """
        if section == common_enums.ModuleSectionType.READING:
            return general_english_models.ReadingQuestion.objects.filter(module_id=module_id)
        elif section == common_enums.ModuleSectionType.LISTENING:
            return general_english_models.ListeningQuestion.objects.filter(module_id=module_id)
        return None

    def _calculate_speaking_score(self, context: str, text: str, max_score: float = 1.0,
                                  tolerance: float = 0.5) -> float:
        """
        Calculate a score for speaking answers based on edit distance.

        Args:
            context: The expected text
            text: The submitted text
            max_score: Maximum possible score
            tolerance: Error tolerance threshold

        Returns:
            Calculated score between 0 and max_score
        """
        if not context or not text:
            return 0.0

        distance = nltk.edit_distance(context.strip().lower(), text.strip().lower())
        max_length = max(len(context), len(text))
        if max_length == 0:
            return max_score

        error_rate = distance / max_length
        return max_score if error_rate <= tolerance else 0.0

    def submit_option_answers(self, data: Dict[str, Any], module_id: int) -> float:
        """
        Submit and score option-based answers (reading, listening).

        Args:
            data: Submission data containing options
            module_id: The module ID

        Returns:
            The calculated score

        Raises:
            ValidationError: If no questions are found
        """
        score = 0
        section = data['section_name']

        general_english_models.ModuleScore.objects.filter(
            module_id=module_id, section=section
        ).delete()

        module_questions = self._get_module_questions(module_id, section)
        if not module_questions:
            raise ValidationError(f"No module questions found for section {section}")

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

        general_english_models.ModuleScore.objects.create(
            module_id=module_id,
            section=section,
            score=score,
        )
        return score

    def submit_speaking_answers(self, data: Dict[str, Any], module_id: int) -> float:
        """
        Submit and score speaking answers.

        Args:
            data: Submission data containing speaking answers
            module_id: The module ID

        Returns:
            The calculated score

        Raises:
            ValidationError: If no speaking exercises are found
        """
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
        """
        Submit and score writing answers using AI evaluation.

        Args:
            data: Submission data containing writing text
            module_id: The module ID

        Returns:
            The calculated score or None if evaluation fails

        Raises:
            ValidationError: If writing evaluation fails or writing not found
        """
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
                score = parsed_response.get('score')

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

        general_english_models.ModuleScore.objects.create(
            module_id=module_id,
            section=section,
            score=final_score,
        )

        return final_score

    def get_score(self, request: Request, module_id: int) -> Dict[str, Any]:
        """
        Retrieve the score for a specific module and section.

        Args:
            request: The HTTP request containing section_name query param
            module_id: The module ID

        Returns:
            Dictionary with section and score

        Raises:
            ValidationError: If score not found or parameters invalid
        """
        section_name = request.query_params.get('section_name')
        if not section_name:
            raise ValidationError("No section_name query parameter provided")

        module = general_english_models.Module.objects.filter(id=module_id).first()
        if not module:
            raise ValidationError(f"Module with ID {module_id} not found")

        module_scores = general_english_models.ModuleScore.objects.filter(module_id=module_id)
        if not module_scores.exists():
            raise ValidationError("No scores found for this module")

        module_section_score = module_scores.filter(section=section_name).first()
        if not module_section_score:
            raise ValidationError(f"No score found for section '{section_name}'")

        return {
            "section": section_name,
            "score": module_section_score.score,
        }
