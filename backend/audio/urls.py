from django.urls import path
from .views import TaskListCreateView, TaskDetailView, TaskDelete, TaskBatchPutView, TaskPostWithoutAudio

app_name = 'audio'

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task_list_create'),
    path('tasks_delete/', TaskDelete.as_view(), name='task_list_delete'),
    path('tasks_without_audio/', TaskPostWithoutAudio.as_view(), name='tasks_without_audio'),
    path('butch_put/', TaskBatchPutView.as_view(), name='task_list_delete'),
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
]
