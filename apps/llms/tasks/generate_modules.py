import logging
import os
import uuid

from celery import shared_task
from django.db import transaction

from apps.common.utils import get_image_url
from apps.general_english import models as general_english_models
from apps.llms import openai_cli, elevenlab_cli
from apps.llms.prompts.listening_generate_prompt import get_listening_generate_prompt
from apps.llms.prompts.module_generate_prompt import get_module_generate_prompt
from apps.llms.prompts.reading_generate_prompt import get_reading_prompt
from apps.llms.prompts.speaking_generate_prompt import get_speaking_prompt
from apps.llms.prompts.writing_generate_prompt import get_writing_prompt
from apps.llms.tasks import parse_json_response
from core.settings import MEDIA_ROOT

logger = logging.getLogger(__name__)
MAX_ATTEMPT = 3


def _create_reading_for_module(created_module, user_level):
    reading_prompt = get_reading_prompt()
    reading_payload = {
        "module_name": created_module.name,
        "module_improvement": created_module.improvement,
        "user_level": user_level,
    }
    attempt = 0
    questions = None
    while attempt < MAX_ATTEMPT:
        response = openai_cli.OpenAICLI().send_request(
            reading_prompt,
            data=(
                    f"Module Improvement: {reading_payload['module_improvement']}" +
                    f"Module Name: {reading_payload['module_name']}" +
                    f"User Level: {reading_payload['user_level']}"
            )
        )
        if hasattr(response, 'text'):
            response_text = response.text
        else:
            response_text = response
        try:
            print(response_text)
            response_data = parse_json_response(response_text)
        except ValueError as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            continue
        questions = response_data.get('questions', [])
        if questions:
            break
        elif attempt == MAX_ATTEMPT - 1:
            logger.error(f"Failed to create reading for module {created_module.name}.")
            return
        attempt += 1

    for question_data in questions:
        image_query = question_data.get('image', '')

        question_obj = general_english_models.ReadingQuestion.objects.create(
            context=question_data.get('context', ''),
            question=question_data.get('question', ''),
            source=question_data.get('source', ''),
            image=get_image_url(image_query),
            module_id=created_module.pk
        )

        options = question_data.get('options', [])
        for option_data in options:
            general_english_models.ReadingOption.objects.create(
                question=question_obj,
                option=option_data.get('option', ''),
                is_correct=option_data.get('is_correct', False),
            )


def _create_writing_for_module(created_module, user_level):
    writing_prompt = get_writing_prompt()
    writing_payload = {
        "module_improvement": created_module.improvement,
        "module_name": created_module.name,
        "user_level": user_level,
    }
    attempt = 0
    writing_data = None

    while attempt < MAX_ATTEMPT:
        response = openai_cli.OpenAICLI().send_request(
            writing_prompt,
            data=(
                f"Module Improvement: {writing_payload['module_improvement']}\n"
                f"Module Name: {writing_payload['module_name']}\n"
                f"User Level: {writing_payload['user_level']}"
            )
        )
        response_text = response.text if hasattr(response, 'text') else response
        print(response_text)
        try:
            parsed = parse_json_response(response_text)
            writing_data = parsed.get('writing')
            if writing_data:
                break
        except ValueError as e:
            logger.error(f"Attempt {attempt + 1} failed to parse JSON: {e}")

        attempt += 1

    if not writing_data:
        logger.error(f"Failed to create writing for module {created_module.name}. No valid response.")
        return

    general_english_models.Writing.objects.create(
        title=writing_data.get('title', ''),
        requirements=writing_data.get('requirements', ''),
        module=created_module,
    )


def _create_listening_for_module(created_module, user_level):
    elevenlab = elevenlab_cli.ElevenLabCli()
    listening_prompt = get_listening_generate_prompt()
    listening_payload = {
        "user_level": user_level,
        "module_improvement": created_module.improvement,
        "module_name": created_module.name,
    }
    attempt = 0
    listening_questions = None
    while attempt < MAX_ATTEMPT:
        response = openai_cli.OpenAICLI().send_request(
            listening_prompt,
            data=(
                    f"Module Improvement: {listening_payload['module_improvement']}" +
                    f"Module Name: {listening_payload['module_name']}" +
                    f"User Level: {listening_payload['user_level']}"
            )
        )
        response_text = response.text if hasattr(response, 'text') else response

        try:
            print(response_text)
            response_data = parse_json_response(response_text)
        except ValueError as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            continue

        listening_questions = response_data.get('listening_questions', [])
        if listening_questions:
            break
        elif attempt == MAX_ATTEMPT - 1:
            logger.error(f"Failed to create listening for module {created_module.name}.")
            return
        attempt += 1

    for question_data in listening_questions:
        context = question_data.get('context', '')
        try:
            voice_bytes = elevenlab.send_request(context)

            if not isinstance(voice_bytes, bytes):
                logger.error(f"Expected bytes from ElevenLabs, got {type(voice_bytes)}")
                continue

            unique_filename = f"{uuid.uuid4()}.wav"
            path = os.path.join(MEDIA_ROOT, unique_filename)

            with open(path, "wb") as f:
                f.write(voice_bytes)

            listening_question_obj = general_english_models.ListeningQuestion.objects.create(
                context=context,
                module_id=created_module.pk,
                audio_question=path
            )

            options_data = question_data.get('options', [])
            for option_data in options_data:
                general_english_models.ListeningOption.objects.create(
                    question=listening_question_obj,
                    option=option_data.get('option', ''),
                    is_correct=option_data.get('is_correct', False)
                )

        except Exception as e:
            logger.error(f"Failed to process listening question: {str(e)}")
            continue


def _create_speaking_for_module(created_module, user_level):
    reading_prompt = get_speaking_prompt()
    speaking_payload = {
        "module_name": created_module.name,
        "module_improvement": created_module.improvement,
        "user_level": user_level,
    }
    attempt = 0
    speaking_data = None
    while attempt < MAX_ATTEMPT:
        response = openai_cli.OpenAICLI().send_request(
            reading_prompt,
            data=(
                    f"Module Improvement: {speaking_payload['module_improvement']}" +
                    f"Module Name: {speaking_payload['module_name']}" +
                    f"User Level: {speaking_payload['user_level']}"
            )
        )
        if hasattr(response, 'text'):
            response_text = response.text
        else:
            response_text = response
        try:
            print(response_text)
            response_data = parse_json_response(response_text)
        except ValueError as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            continue

        speaking_data = response_data.get('speaking', {})
        if speaking_data:
            break
        elif attempt == MAX_ATTEMPT - 1:
            logger.error(f"Failed to create reading for module {created_module.name}.")
            return
        attempt += 1
    sentences = speaking_data.get('sentences', [])
    for sentence in sentences:
        general_english_models.Speaking.objects.create(
            context=sentence.get('text', ''),
            module_id=created_module.pk
        )


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def generate_modules(self, user_course_id, score, user_answers_log):
    if score >= 8:
        user_level = "Advanced"  # C1-C2
    elif score >= 5:
        user_level = "Intermediate"  # B1-B2
    else:
        user_level = "Beginner"  # A1-A2
    prompt = get_module_generate_prompt()
    module_payload = {
        "user_scored_english_level": user_level,
        "user_answers_log_to_test": user_answers_log,
        "user_score": score,
        "max_possible_score": 10,
        "score_percentage": (score / 10) * 100 if score > 0 else 0,
    }

    try:
        user_course = general_english_models.UserProgress.objects.get(id=user_course_id)
    except general_english_models.UserProgress.DoesNotExist as e:
        logger.error(f"User course with ID {user_course_id} not found.")
        raise ValueError(str(e))

    try:
        attempt = 0
        modules_data = None
        while attempt < MAX_ATTEMPT:
            response = openai_cli.OpenAICLI().send_request(
                prompt,
                data=f"""
                    {''.join([f"{key}:{values}" for key, values in module_payload.items()])}
                """
            )
            response_text = response.text if hasattr(response, 'text') else response

            try:
                response_data = parse_json_response(response_text)
            except ValueError as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                attempt += 1
                continue

            print(response_data)
            modules_data = response_data.get('modules', [])
            if modules_data:
                break
            elif attempt == MAX_ATTEMPT:
                logger.error(f"Failed to generate modules for user course {user_course_id}.")
                return
            attempt += 1

        with transaction.atomic():
            general_english_models.Module.objects.filter(user_course_id=user_course_id).delete()
            modules = []
            for i, module_info in enumerate(modules_data, start=1):
                created_module = general_english_models.Module.objects.create(
                    name=module_info.get('name', f'Module {i}'),
                    user_course=user_course,
                    improvement=module_info.get('improvement', ''),
                    has_writing=True,
                    has_reading=True,
                    has_listening=True,
                    has_speaking=True
                )

                _create_reading_for_module(created_module, user_level)
                _create_writing_for_module(created_module, user_level)
                _create_listening_for_module(created_module, user_level)
                _create_speaking_for_module(created_module, user_level)
                modules.append(created_module)
            user_course.last_module = modules[0]
            user_course.level = user_level
            user_course.save()
            return True

    except Exception as e:
        logger.error(f"Error generating modules: {str(e)}", exc_info=True)
        retry_count = self.request.retries
        countdown = 5 * (2 ** retry_count)
        raise self.retry(exc=e, countdown=countdown, max_retries=3)
