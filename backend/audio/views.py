from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializer import TaskSerializer, TaskSerializerGet, TaskIDSerializer, BatchUpdateTaskSerializer, TaskSerializerWithoutAudio
from users.models import UserModel
from .utils import transcribes_audio_into_text



class TaskListCreateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = TaskSerializer

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        user = UserModel.objects.get(id=data['user'])
        data['user'] = user.id

        if 'audio_file' not in request.FILES:
            return Response({'error': 'Audio file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            audio_file = request.FILES['audio_file']

            try:
                prompts = transcribes_audio_into_text(audio_file)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            Task.objects.create(
                user=user,
                title=serializer.validated_data['title'],
                audio_file=audio_file,
                prompts=prompts,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskBatchPutView(APIView):
    permission_classes = [AllowAny]
    serializer_class = BatchUpdateTaskSerializer

    def put(self, request):
        serializer = BatchUpdateTaskSerializer(data=request.data)

        if serializer.is_valid():
            task_ids = serializer.validated_data['task_ids']
            title = serializer.validated_data.get('title', None)
            prompts = serializer.validated_data.get('prompts', None)

            tasks = Task.objects.filter(id__in=task_ids)

            if not tasks.exists():
                return Response({'error': 'No tasks found for provided IDs.'}, status=status.HTTP_404_NOT_FOUND)

            found_ids = set(tasks.values_list('id', flat=True))
            not_found_ids = set(task_ids) - found_ids

            update_data = {}
            if title:
                update_data['title'] = title
            if prompts:
                update_data['prompts'] = prompts

            tasks.update(**update_data)

            return Response({
                'updated_count': len(found_ids),
                'not_found_ids': list(not_found_ids)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskPostWithoutAudio(APIView):
    serializer_class = TaskSerializerWithoutAudio
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()

        serializer = TaskSerializerWithoutAudio(data=data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDelete(APIView):
    permission_classes = [AllowAny]
    serializer_class = TaskIDSerializer

    def post(self, request):
        serializer = TaskIDSerializer(data=request.data)

        if serializer.is_valid():
            task_ids = serializer.validated_data['task_ids']  # Получаем проверенные ID задач

            tasks = Task.objects.filter(id__in=task_ids)

            if not tasks.exists():
                return Response({'error': 'No tasks found for provided IDs.'}, status=status.HTTP_404_NOT_FOUND)

            found_ids = set(tasks.values_list('id', flat=True))
            not_found_ids = set(task_ids) - found_ids

            deleted_count, _ = tasks.delete()

            return Response({
                'deleted_count': deleted_count,
                'not_found_ids': list(not_found_ids)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    serializer_class = TaskSerializerGet

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        serializer = TaskSerializerGet(task)
        return Response(serializer.data)



