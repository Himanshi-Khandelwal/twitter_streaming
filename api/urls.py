from django.conf.urls import url, include
from api import views

urlpatterns = [
    url('tasks/', views.TaskViewSet.as_view(), name='task_list'),
    url(r'^task-filter/', views.TaskFilterSet.as_view(), name='task_filter'),
    url(r'^task-csv/', views.GetCSV.as_view(), name='getcsv'),
]