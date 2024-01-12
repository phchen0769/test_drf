from rest_framework import serializers
from .models import Students, Answers, Questions, Papers


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = "__all__"


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = "__all__"


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = "__all__"


class PapersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Papers
        fields = "__all__"
