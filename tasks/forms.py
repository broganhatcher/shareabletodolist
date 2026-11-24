from django import forms
from .models import task, TaskGroup
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class TaskForm(forms.ModelForm):
    class Meta:
        model = task
        fields = ("text", "tag", "group")
        widgets = {
            "text": forms.TextInput(attrs={"placeholder": "Task"}),
            "tag": forms.TextInput(attrs={"placeholder": "field or focus"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].required = False
        if user is not None:
            self.fields["group"].queryset = TaskGroup.objects.filter(members=user)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "display_name", "bio")


class ShareTaskForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Username to share with"}),
    )
    
class AddGroupMemberForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Username to add"}),
    )
