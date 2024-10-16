from django.db import models
from users.models import UserModel

class Task(models.Model):
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio_files/', null=True, blank=True)
    user = models.ForeignKey(to=UserModel, blank=True, null=True, on_delete=models.CASCADE)  # Убедимся, что ссылка на пользователя корректна
    prompts = models.JSONField(default=list)  # Поле для хранения промптов в формате JSON

    def __str__(self):
        return self.title
