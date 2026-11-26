from django import forms
from .models import task, TaskList

class TaskForm(forms.ModelForm):
    class Meta:
        model = task
        fields = ("text", "tag")
        widgets = {
            "text": forms.TextInput(attrs={"placeholder": "Task"}),
            "tag": forms.TextInput(attrs={"placeholder": "field or focus"}),
        }

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "display_name", "bio")

class ShareTaskForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Username to share with"}),
    )

class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ("name",)


class ShareListForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"placeholder": "Username to add"}))
