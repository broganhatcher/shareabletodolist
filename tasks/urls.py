from django.urls import path
from . import views
from .views import taskCreateView, taskListView
from django.contrib.auth import views as auth_views


urlpatterns = [
        path('', views.home_page, name='home'),
        path("tasks/new/", taskCreateView.as_view(), name="newtask"),
        path("tasks/", taskListView.as_view(), name="tasklist"),
        path('register/', views.register, name='register'),
        path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        path("tasks/<int:pk>/delete/", views.taskDeleteView.as_view(), name="deletetask"),
        path("tasks/<int:pk>/share/", views.share_task, name="sharetask"),
        path("tasks/<int:pk>/unshare/<int:user_id>/", views.unshare_task, name="unsharetask"),


    path("lists/", views.project_lists, name="projectlists"),
    path("lists/new/", views.create_list, name="newlist"),
    path("lists/<int:pk>/", views.list_detail, name="listdetail"),
    path("lists/<int:pk>/share/", views.share_list, name="sharelist"),
    path("lists/<int:pk>/tasks/new/", views.create_project_task, name="newprojecttask"),
    path("lists/<int:pk>/tasks/<int:task_id>/delete/", views.delete_project_task, name="deleteprojecttask"),
]
