from django import forms
from django.forms import formset_factory

from apps.common import enums
from apps.courses import models as courses_models


class QuestionOptionForm(forms.Form):
    option = forms.CharField()
    is_correct = forms.BooleanField(required=False)


class QuestionForm(forms.Form):
    question = forms.CharField(label="Вопрос")
    question_type = forms.ChoiceField(
        choices=enums.QuestionType.choices,
        label="Тип вопроса"
    )


class AdminTestForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=courses_models.Course.objects.all(),
        widget=forms.HiddenInput()
    )


QuestionOptionFormSet = formset_factory(QuestionOptionForm, extra=1)
QuestionFormSet = formset_factory(QuestionForm, extra=1)
