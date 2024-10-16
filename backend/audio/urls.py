from django.urls import path
from .views import TaskListCreateView, TaskDetailView, TaskDelete, TaskBatchPutView

app_name = 'audio'

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task_list_create'),
    path('tasks_delete/', TaskDelete.as_view(), name='task_list_delete'),
    path('butch_put/', TaskBatchPutView.as_view(), name='task_list_delete'),
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
]
