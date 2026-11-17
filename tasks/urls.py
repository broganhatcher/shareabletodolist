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


]
