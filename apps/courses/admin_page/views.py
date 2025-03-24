from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.common import enums
from apps.courses import models as courses_models
from apps.general_english.models import TrialQuestion, TrialOption
from .forms import AdminTestForm, QuestionFormSet


class CreateTestAdmin(View):
    def get(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(courses_models.Course, pk=course_id)
        test_form = AdminTestForm(initial={"course": course.pk})
        question_formset = QuestionFormSet(prefix="q")

        return render(request, "admin/trial_test_form.html", {
            "test_form": test_form,
            "question_formset": question_formset,
            "course_obj": course
        })

    def post(self, request, course_id, *args, **kwargs):
        course = get_object_or_404(courses_models.Course, pk=course_id)
        test_form = AdminTestForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix="q")

        if not test_form.is_valid() or not question_formset.is_valid():
            return render(request, "admin/trial_test_form.html", {
                "test_form": test_form,
                "question_formset": question_formset,
                "course_obj": course
            })

        for i, form in enumerate(question_formset):
            if not form.cleaned_data:
                continue

            question_text = form.cleaned_data.get("question")
            question_type = form.cleaned_data.get("question_type")
            if not question_text or not question_type:
                continue

            question = TrialQuestion.objects.create(
                course=course,
                question=question_text,
                question_type=question_type
            )

            if question_type == enums.QuestionType.SINGLE_CHOICE:
                correct_index = request.POST.get(f"question-{i}-correct")

                j = 0
                while True:
                    key = f"question-{i}-option-{j}-text"
                    if key not in request.POST:
                        break

                    option_text = request.POST[key]
                    if option_text:
                        TrialOption.objects.create(
                            question=question,
                            option=option_text,
                            is_correct=(str(j) == str(correct_index))
                        )
                    j += 1

        return redirect(request.META.get('HTTP_REFERER'))
