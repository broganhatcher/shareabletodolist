from django.urls import path
from . import views
from .views import taskCreateView, taskListView, GroupListView, GroupCreateView
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
        path("groups/", GroupListView.as_view(), name="group_list"),
        path("groups/new/", GroupCreateView.as_view(), name="group_create"),
        path("groups/<int:pk>/manage/", views.manage_group, name="manage_group"),
        path("groups/<int:pk>/remove/<int:user_id>/", views.remove_group_member, name="remove_group_member"),
        path("groups/<int:pk>/leave/", views.leave_group, name="leave_group"),
        path("groups/<int:pk>/delete/", views.GroupDeleteView.as_view(), name="delete_group"),


]
