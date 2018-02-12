from django.urls import path, include, re_path
from api import views

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    re_path(r'^tasks-filter/', views.task_filter, name='task_filter'),
]
