from django.conf.urls import url, include
from api import views

urlpatterns = [
    url('tasks/', views.TaskViewSet.as_view({"get": "list"}), name='task_list'),
    url(r'^tasks-filter/', views.task_filter, name='task_filter'),
]