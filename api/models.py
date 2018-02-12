from django.db import models
from jsonfield import JSONField
# Create your models here.
class Task(models.Model):
    search = models.CharField(max_length=100)

class TaskFilter(models.Model):
    filters = models.CharField(max_length=100, null =True)
    retweet_count= models.CharField(max_length=100, null =True)
    word =  models.CharField(max_length=100, null =True)
