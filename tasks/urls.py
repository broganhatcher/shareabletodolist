from django.urls import path
from . import views
from .views import taskCreateView, taskListView


urlpatterns = [
        path('', views.home_page, name='home'),
        path("tasks/new/", taskCreateView.as_view(), name="newtask"),
        path("tasks/", taskListView.as_view(), name="tasklist"),
]