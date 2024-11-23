from rest_framework import serializers
from api import models
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    status = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.TaskModel
        fields = '__all__'
        

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']
        