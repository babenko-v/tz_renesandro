from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'audio_file', 'user']

class TaskSerializerWithoutAudio(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'prompts']

class TaskSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'audio_file', 'user', 'prompts']

class TaskIDSerializer(serializers.Serializer):
    task_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        error_messages={
            'required': 'Task IDs are required.',
            'empty': 'Task IDs cannot be empty.'
        }
    )

class BatchUpdateTaskSerializer(serializers.Serializer):
    task_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text="IDs of tasks to update"
    )
    title = serializers.CharField(required=False, allow_blank=True)
    prompts = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    def validate(self, data):
        if not data.get('title') and not data.get('prompts'):
            raise serializers.ValidationError("At least one of 'title' or 'prompts' must be provided.")
        return data