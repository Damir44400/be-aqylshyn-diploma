import uuid

from django.core.files.base import ContentFile
from django.core.management import BaseCommand

from apps.common import enums
from apps.ielts import models
from apps.llms import openai_cli, elevenlab_cli
from apps.llms.tasks import parse_json_response


class Command(BaseCommand):
    TEST_GENERATOR_PROMPT = """
    You are an expert IELTS content creator.

    - Generate exactly 4 unique IELTS tests for the sub-module user will provide u difficulty of sub module.
    - Return a strictly valid JSON object in the following format:

    {
      "tests": [
        {
          "test_name": "<engaging, specific title>",
          "for_sub_module": "{difficulty}",
          "description": "<one-sentence overview of skills tested and topic>"
        },
        ...
      ]
    }

    - Each `test_name` must be unique.
    - `for_sub_module` must exactly match "{difficulty}".
    - Description must clearly mention the IELTS skills (e.g., reading comprehension, essay writing, listening).
    - Respond ONLY with the JSON object. No extra explanation, notes, or text.
    - The JSON must be syntactically valid and parsable.
        """

    READING_GENERATOR_PROMPT = """
    You are generating IELTS Reading passages and questions.
    GENERATE REAL IELTS READING PASSAGES AND QUESTIONS
    AND GENERATE IN EACH PASSAGE DIFFERENCE TYPE OF QUESTION NOT ONLY OPTIONS TYPE 

    User will provide the test details
        
    Generate exactly 3 passages, each with exactly 10 questions.

    RESPONSE FORMAT:
    {
      "passages": [
        {
          "passage_number": 1,
          "title": "<academic topic>",
          "content": "<250-350 academic words>",
          "questions": [
            {
              "question_content": "<clear academic question>",
              "question_type": "OPTIONS" | "FILL" | "SELECT_INSERT",
              (based on type, include exactly one of the following:)
              - For OPTIONS:
                  "options": [
                      { "option": "<text>", "is_correct": true/false },
                      ...
                  ]
              - For FILL:
                  "fill_blank": {
                      "answers": ["<answer1>", "<answer2>", ...]
                  }
              - For SELECT_INSERT:
                  "select_insert": {
                      "correct_answer": "<full correct sentence>",
                      "options": ["<option1>", "<option2>", "<option3>", "<option4>", "<option5>"]
                  }
            }
          ]
        }
      ]
    }
    
    - Each passage must have exactly 10 questions.
    - Each question must provide the correct answer structure based on its type.
    - No duplicate content across passages or questions.
    - Language must be clear, academic, and error-free.
    - Respond ONLY with the JSON object. No extra explanation or notes.
    - JSON must be strictly valid and parsable.
    """

    LISTENING_GENERATOR_PROMPT = """
    You are generating IELTS Listening parts and questions.
    GENERATE REAL IELTS READING PASSAGES AND QUESTIONS
    AND GENERATE IN EACH PASSAGE DIFFERENCE TYPE OF QUESTION NOT ONLY OPTIONS TYPE
     
    User will provide the test details
        
    Generate exactly 4 parts, each with exactly 5 questions.

    RESPONSE FORMAT:
    {
      "title": "<academic topic>",
      "audio_file_context" : "2000-3000 words"
      "parts": [
        {
          "part": 1,
          "questions": [
            {
              "question_content": "<clear academic question>",
              "question_type": "OPTIONS" | "FILL" | "SELECT_INSERT",
              (based on type, include exactly one of the following:)
              - For OPTIONS:
                  "options": [
                      { "option": "<text>", "is_correct": true/false },
                      ...
                  ]
              - For FILL:
                  "fill_blank": {
                      "answers": ["<answer1>", "<answer2>", ...]
                  }
            }
          ]
        }
      ]
    }
    
    - Each passage must have exactly 10 questions.
    - Each question must provide the correct answer structure based on its type.
    - No duplicate content across passages or questions.
    - Language must be clear, academic, and error-free.
    - Respond ONLY with the JSON object. No extra explanation or notes.
    - JSON must be strictly valid and parsable.
    """

    def handle(self, *args, **options):
        openai_client = openai_cli.OpenAICLI()
        elevenlab_client = elevenlab_cli.ElevenLabCli()

        sub_modules = models.IeltsSubModule.objects.all()
        models.IeltsTest.objects.all().delete()

        for submodule in sub_modules:
            self.process_submodule(openai_client, elevenlab_client, submodule)

    def process_submodule(self, openai_client, elevenlab_client, submodule):
        difficulty = submodule.difficulty.upper()

        raw_tests = openai_client.send_request(
            self.TEST_GENERATOR_PROMPT,
            data=f"The sub module difficulty is: {difficulty}",
            model="gpt-4o-mini"
        )
        tests = parse_json_response(raw_tests).get("tests", [])

        for order, test_data in enumerate(tests, start=1):
            test = models.IeltsTest.objects.create(
                name=test_data["test_name"],
                sub_model=submodule,
                order=order
            )
            self.generate_reading(openai_client, test, submodule.difficulty, test_data["description"])
            self.generate_listening(openai_client, elevenlab_client, test, submodule.difficulty,
                                    test_data["description"])

    def generate_reading(self, openai_client, test, difficulty, description):
        reading_raw = openai_client.send_request(
            self.READING_GENERATOR_PROMPT,
            data=f"The test details: title {test.name}\n difficulty: {difficulty}\n focus: {description}",
            model="gpt-4.1-2025-04-14"
        )
        passages = parse_json_response(reading_raw).get("passages", [])

        for passage_data in passages:
            passage = models.IeltsReading.objects.create(
                title=passage_data["title"],
                content=passage_data["content"],
                passage_number=passage_data["passage_number"],
                test=test
            )
            self.create_reading_questions(passage, passage_data["questions"])

    def create_reading_questions(self, passage, questions):
        for qdata in questions:
            question = models.IeltsReadingQuestion.objects.create(
                question_content=qdata["question_content"],
                question_type=qdata["question_type"],
                reading=passage
            )
            self.create_reading_question_detail(question, qdata)

    def create_reading_question_detail(self, question, qdata):
        if question.question_type == enums.IeltsReadingQuestionType.OPTIONS:
            for opt in qdata["options"]:
                models.IeltsReadingOption.objects.create(
                    option=opt["option"],
                    is_correct=opt["is_correct"],
                    question=question,
                )
        elif question.question_type == enums.IeltsReadingQuestionType.SELECT_INSERT:
            select_insert = qdata["select_insert"]
            models.IeltsReadingSelectInsert.objects.create(
                question=question,
                correct_answer=select_insert["correct_answer"],
                options=select_insert["options"],
            )
        elif question.question_type == enums.IeltsReadingQuestionType.FILL_BLANK:
            fill_blank = qdata["fill_blank"]
            models.IeltsReadingFillBlank.objects.create(
                question=question,
                answer=fill_blank["answers"],
            )

    def generate_listening(self, openai_client, elevenlab_client, test, difficulty, description):
        listening_raw = openai_client.send_request(
            self.LISTENING_GENERATOR_PROMPT,
            data=f"The test details: title {test.name}\n difficulty: {difficulty}\n focus: {description}",
            model="gpt-4.1-2025-04-14"
        )
        listening_data = parse_json_response(listening_raw)

        audio_context = listening_data.get("audio_file_context")
        title = listening_data.get("title")
        if not audio_context:
            return

        voice_bytes = elevenlab_client.send_request(audio_context)
        if not isinstance(voice_bytes, bytes):
            return

        audio_file = ContentFile(voice_bytes, name=f"{uuid.uuid4()}.mp3")
        listening_obj = models.IeltsListening.objects.create(
            title=title,
            audio_file=audio_file,
            test=test,
        )

        for part_data in listening_data.get("parts", []):
            self.create_listening_part(listening_obj, part_data)

    def create_listening_part(self, listening_obj, part_data):
        part = models.IeltsListeningPart.objects.create(
            part=int(part_data["part"]),
            listening=listening_obj
        )
        for qdata in part_data["questions"]:
            question = models.IeltsListeningQuestion.objects.create(
                listening_part=part,
                question_content=qdata["question_content"],
                question_type=qdata["question_type"],
            )
            self.create_listening_question_detail(question, qdata)

    def create_listening_question_detail(self, question, qdata):
        if question.question_type == enums.IeltsListeningQuestionType.OPTIONS:
            for opt in qdata["options"]:
                models.IeltsListeningOption.objects.create(
                    option=opt["option"],
                    is_correct=opt["is_correct"],
                    question=question,
                )
        elif question.question_type == enums.IeltsListeningQuestionType.FILL_BLANK:
            fill_blank = qdata["fill_blank"]
            models.IeltsListeningFillBlank.objects.create(
                question=question,
                answer=fill_blank["answers"],
            )
