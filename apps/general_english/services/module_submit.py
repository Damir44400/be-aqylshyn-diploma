import nltk
from rest_framework.exceptions import ValidationError

from apps.common import enums as common_enums, enums
from apps.general_english import models as general_english_models, models
from apps.llms import openai_cli
from apps.llms.prompts.essay_checker_prompt import get_essay_checker_prompt
from apps.llms.tasks import parse_json_response

MAX_ATTEMPTS = 3


class ModuleSubmitService:
    def _get_module_questions(self, module_id, section):
        if section == common_enums.ModuleSectionType.READING:
            return general_english_models.ReadingQuestion.objects.filter(module_id=module_id)
        elif section == common_enums.ModuleSectionType.LISTENING:
            return general_english_models.ListeningQuestion.objects.filter(module_id=module_id)
        return None

    def _calculate_speaking_score(self, context, text, max_score=1.0, tolerance=0.5):
        if not context or not text:
            return 0.0

        distance = nltk.edit_distance(context, text)
        max_length = max(len(context), len(text))
        if max_length == 0:
            return max_score

        error_rate = distance / max_length
        return max_score if error_rate <= tolerance else 0.0

    def submit_option_answers(self, data, module_id):
        score = 0
        section = data['section_name']

        existing_score = general_english_models.ModuleScore.objects.filter(
            module_id=module_id, section=section
        ).first()
        if existing_score:
            existing_score.delete()

        module_questions = self._get_module_questions(module_id, section)
        if not module_questions:
            return 0

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

    def submit_speaking_answers(self, data, module_id):
        score = 0
        section = data['section_name']

        general_english_models.ModuleScore.objects.filter(
            module_id=module_id, section=section
        ).delete()

        db_speakings = general_english_models.Speaking.objects.filter(module_id=module_id)
        if not db_speakings:
            return 0

        for answer in data.get("answers", []):
            speaking_id = answer.get('speaking_id')
            text = answer.get('text')

            speaking = db_speakings.filter(id=speaking_id).first()
            if not speaking:
                continue

            score += self._calculate_speaking_score(speaking.context, text)

        general_english_models.ModuleScore.objects.create(
            module_id=module_id,
            section=section,
            score=score,
        )
        return score

    def submit_writing_answers(self, data, module_id):
        section = data['section_name']

        general_english_models.ModuleScore.objects.filter(
            module_id=module_id, section=section
        ).delete()

        writing_data = data.get("writing")
        module = (
            general_english_models.Module.objects
            .filter(id=module_id)
            .prefetch_related('writing')
            .first()
        )
        if not module or not module.writing:
            return None

        db_writing = module.writing.first()

        prompt = get_essay_checker_prompt()

        score = None
        for _attempt in range(MAX_ATTEMPTS):
            response = openai_cli.OpenAICLI().send_request(
                system_prompt=prompt,
                data=f"requirements: {db_writing.requirements}\nuser answer: {writing_data}"
            )
            response_text = getattr(response, 'text', response)

            try:
                parsed_response = parse_json_response(response_text)
            except ValueError:
                continue
            print(parsed_response)
            score = parsed_response.get('score')
            if score is not None:
                break

        if score is None:
            raise ValidationError("Couldn't get a valid score from the writing checker.")

        final_score = float(score)

        models.ModuleScore.objects.create(
            module_id=module_id,
            section=enums.ModuleSectionType.WRITING,
            score=final_score,
        )

        return float(score)

    def get_score(self, request, module_id):
        section_name = request.query_params.get('section_name')
        if not section_name:
            raise ValidationError("No section_name query param provided.")

        module = general_english_models.Module.objects.filter(id=module_id).first()
        if not module:
            raise ValidationError(f"Module with ID {module_id} not found.")

        module_score_qs = models.ModuleScore.objects.filter(module_id=module_id)
        if not module_score_qs.exists():
            raise ValidationError("No scores found for this module.")

        module_section_score = module_score_qs.filter(section=section_name).first()
        if not module_section_score:
            raise ValidationError("You have not passed this section yet.")

        return {
            "section": section_name,
            "score": module_section_score.score,
        }
