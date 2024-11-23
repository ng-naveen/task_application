from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import TaskSerializer, UserSerializer
from api.models import TaskModel
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import authentication, permissions


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serialized_data = UserSerializer(data=request.data)
        if serialized_data.is_valid():
            User.objects.create_user(**serialized_data.validated_data)
            return Response(data=serialized_data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serialized_data.errors)


class TaskModelViewSetView(ModelViewSet):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = TaskModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        task_objs = TaskModel.objects.filter(user=request.user)
        deserialized_data = TaskSerializer(task_objs, many=True)
        return Response(data=deserialized_data.data)

    @action(methods=['GET'], detail=False)
    def finished_task(self, request, *args, **kwargs):
        task_objs =TaskModel.objects.filter(status=True)
        deserialized_data = TaskSerializer(task_objs, many=True)
        return Response(data=deserialized_data.data)
    
    @action(methods=['GET'], detail=False)
    def pending_task(self, request, *args, **kwargs):
        task_objs = TaskModel.objects.filter(status=False)
        deserialized_data = TaskSerializer(task_objs, many=True)
        return Response(data=deserialized_data.data)
    

    @action(methods=['POST'], detail=True)
    def mark_as_done(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        TaskModel.objects.filter(id=task_id).update(status=True)
        return Response(data='Updated')
    

# class TaskView(APIView):
#     def get(self, request, *args, **kwargs):
#         task_objs = TaskModel.objects.all()
#         deserialized_data = TaskSerializer(task_objs, many=True)
#         return Response(data=deserialized_data.data)
    
#     def post(self, request, *args, **kwargs):
#         serialized_data = TaskSerializer(data=request.data)
#         if serialized_data.is_valid():
#             serialized_data.save()
#             return Response(data=serialized_data.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(data=serialized_data.errors)
        
# class TaskDetailView(APIView):
#     def get(self, request, *args, **kwargs):
#         task_id = kwargs.get('id')
#         task_obj = TaskModel.objects.get(id=task_id)
#         deserialized_data = TaskSerializer(task_obj, many=False)
#         return Response(data=deserialized_data.data)
    
#     def put(self, request, *args, **kwargs):
#         task_id = kwargs.get('id')
#         task_obj = TaskModel.objects.get(id=task_id)
#         serialized_data = TaskSerializer(data=request.data, instance=task_obj)
#         if serialized_data.is_valid():
#             serialized_data.save()
#             return Response(data=serialized_data.data)
#         else:
#             return Response(data=serialized_data.errors)
    
#     def delete(self, request, *args, **kwargs):
#         task_id = kwargs.get('id')
#         TaskModel.objects.get(id=task_id).delete()
#         return Response(data='Deleted', status=status.HTTP_204_NO_CONTENT)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   


# class TaskViewSetView(ViewSet):
#     def create(self, request, *args, **kwargs):
#         serialized_data = TaskSerializer(data=request.data)
#         if serialized_data.is_valid():
#             serialized_data.save()
#             return Response(data=serialized_data.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(data=serialized_data.errors)

#     def list(self, request, *args, **kwargs):
#         task_objs = TaskModel.objects.all()
#         deserialized_data = TaskSerializer(task_objs, many=True)
#         return Response(data=deserialized_data.data)
        
#     def update(self, request, *args, **kwargs):
#         task_id = kwargs.get('pk')
#         task_obj = TaskModel.objects.get(id=task_id)
#         serialized_data = TaskSerializer(data=request.data, instance=task_obj)
#         if serialized_data.is_valid():
#             serialized_data.save()
#             return Response(data=serialized_data.data)
#         else:
#             return Response(data=serialized_data.errors)
        
#     def retrive(self, request, *args, **kwargs):
#         task_id = kwargs.get('pk')
#         task_obj = TaskModel.objects.get(id=task_id)
#         deserialized_data = TaskSerializer(task_obj, many=False)
#         return Response(data=deserialized_data.data)
    
#     def destroy(self, request, *args, **kwargs):
#         task_id = kwargs.get('pk')
#         TaskModel.objects.get(id=task_id).delete()
#         return Response(data='Deleted', status=status.HTTP_204_NO_CONTENT)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
