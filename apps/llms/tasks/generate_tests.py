from apps.common import enums as common_enums
from apps.courses import models as courses_models
from apps.courses.course_level_definer import models as course_level_definer


def generate_tests(user_id):
    user_answers = (
        course_level_definer
        .UserCourseLevelDefinerChoice
        .objects
        .filter(
            user_id=user_id,
            question__question_type=common_enums.QuestionType.TEXT_ANSWER
        )
    )
    user_level = courses_models.UserCourseLevel.objects.filter(passed_by_id=user_id).first()

    score = user_level.score
    course = user_level.course

    prompts = \
    """
    Ты бот ассистент который генерить тест по модулям и по английском смотря на уровень пользователя и его цели
    формат ответа должна быть таким:
    [
        {
            "module_name" : string,
            "order" : int
            "sections" : {
                "writing" : [
                    {
                        "title" : string,
                        "description" : string,
                        "content" : string
                    },
                ],
                "reading" : [
                    {
                        "title" : string,
                        "article_source" : string,
                        "description" : string,
                        "need_image": bool,
                        "options": [
                            {
                                "option": string,
                                "is_correct": bool, 
                            }
                        ]
                    },
                ],
                "speaking" : [
                    {
                        "question" : string,
                    }
                ],
                "listening" : [
                ]
            }
        }
    ]
    """
