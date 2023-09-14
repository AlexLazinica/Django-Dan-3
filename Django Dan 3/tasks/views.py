from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from tasks.models import Task
from django.http import Http404
from tasks.serializers import TaskSerializer

class TaskListView(APIView):
    def get(self, request):
        all_tasks = Task.objects.all()
        task_serialized = TaskSerializer(all_tasks, many=True)
        return Response(task_serialized.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            #sacuvati objekat u bazi
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    def get_object(self, pk):
        try:
            task_object = Task.objects.get(id=pk)
            return task_object
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)

    def patch(self, request, pk):
        task = self.get_object(ok)
        serializer = TaskSerializer(task, data = request.data , partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)