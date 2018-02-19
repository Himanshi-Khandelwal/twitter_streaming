from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongoserializers

from api.models import Task, Tweet, Users


class TaskSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TweetSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = Tweet
        fields = '__all__'

class UserSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = Users
        fields = '__all__'