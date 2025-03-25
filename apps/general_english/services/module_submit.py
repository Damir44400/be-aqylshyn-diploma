import math

import nltk

from apps.common import enums as common_enums
from apps.general_english import models as general_english_models
from apps.llms.tasks.essay_checker import essay_checker


class ModuleSubmitService:
    def _get_module_questions(self, module_id, section):
        if section == common_enums.ModuleSectionType.READING:
            return general_english_models.ReadingQuestion.objects.filter(module_id=module_id)
        elif section == common_enums.ModuleSectionType.LISTENING:
            return general_english_models.ListeningQuestion.objects.filter(module_id=module_id)
        return None

    def _calculate_speaking_score(self, context, text, max_score=1.0):
        if not context or not text:
            return 0.0

        distance = nltk.edit_distance(context, text)
        max_length = max(len(context), len(text))

        if max_length == 0:
            return max_score

        normalized_score = max_score * math.exp(-distance / max_length)

        return max(0, min(normalized_score, max_score))

    def submit_option_answers(self, data, module_id):
        score = 0
        section = data['section_name']

        module_score = general_english_models.ModuleScore.objects.filter(
            module_id=module_id, section=section
        ).first()

        if module_score:
            module_score.delete()

        module_questions = self._get_module_questions(module_id, section)

        if not module_questions:
            return 0

        for option in data.get('options', []):
            question_id = option.get('question_id')
            option_id = option.get('option_id')

            question = module_questions.filter(id=question_id).prefetch_related('options').first()

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
            module=module_id, section=section
        ).delete()

        db_speakings = general_english_models.Speaking.objects.filter(module=module_id)
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
        module = general_english_models.Module.objects.filter(
            module_id=module_id
        ).prefetch_related('writing').first()
        writing = module.writing

        if not writing:
            return None

        task_id = essay_checker.delay(writing.id, writing_data.get("text"))

        return task_id
