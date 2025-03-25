from celery import shared_task

from apps.common import enums
from apps.general_english import models
from apps.llms import openai_cli
from apps.llms.prompts.essay_checker_prompt import get_essay_checker_prompt
from apps.llms.tasks import parse_json_response

MAX_ATTEMPTS = 3


@shared_task(ignore_result=True)
def essay_checker(writing_id, user_answer):
    writing = models.Writing.objects.filter(id=writing_id).first()
    if writing is None:
        return
    prompt = get_essay_checker_prompt()
    attempt = 0
    score = 0
    while attempt < MAX_ATTEMPTS:
        response = openai_cli.OpenAICLI().send_request(
            system_prompt=prompt,
            data=f"requirements: {writing.requirements}\nuser answer: {user_answer}"
        )

        response_text = response.text if hasattr(response, 'text') else response

        try:
            parsed_response = parse_json_response(response_text)
        except ValueError:
            attempt += 1
            continue

        writing = parsed_response.get('writing')
        score = parsed_response.get('score')
        if score:
            break

        attempt += 1

    module_score = models.ModuleScore.objects.create(
        module=writing.module,
        section=enums.ModuleSectionType.WRITING,
        score=float(score),
    )

    return module_score
