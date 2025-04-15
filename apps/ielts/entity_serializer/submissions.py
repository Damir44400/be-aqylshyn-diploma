from rest_framework import serializers

from apps.ielts.entity_models.attempts.ielts_test_attempt import IeltsTestAttempt
from apps.ielts.entity_models.attempts.listening_submissions import IeltsListeningSubmission
from apps.ielts.entity_models.attempts.reading_submissions import IeltsReadingSubmission
from apps.ielts.entity_models.attempts.writing_submissions import IeltsWritingSubmission


class IeltsTestAttemptSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = IeltsTestAttempt
        fields = ['id', 'user', 'test', 'started_at', 'completed_at']
        read_only_fields = ['id', 'started_at', 'completed_at']


class IeltsAttemptCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = IeltsTestAttempt
        fields = ['id', 'completed_at']
        read_only_fields = ['id', 'completed_at']


class IeltsReadingSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IeltsReadingSubmission
        fields = [
            'id',
            'attempt',
            'question',
            'selected_option',
            'fill_blank_answer',
            'select_insert_answer'
        ]
        read_only_fields = ['id', 'attempt', 'question']


class IeltsListeningSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IeltsListeningSubmission
        fields = [
            'id',
            'attempt',
            'question',
            'selected_option',
            'fill_blank_answer'
        ]
        read_only_fields = ['id', 'attempt', 'question']


class IeltsWritingSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IeltsWritingSubmission
        fields = [
            'id',
            'attempt',
            'writing',
            'answer_text'
        ]
        read_only_fields = ['id', 'attempt', 'writing']
