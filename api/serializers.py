from rest_framework import serializers

from api.models import Task, TaskFilter


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['search']


class TaskFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFilter
        fields = ['filters','retweet_count','word']
