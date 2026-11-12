from django import forms
from .models import task

class TaskForm(forms.ModelForm):
    class Meta:
        model = task
        fields = ("text", "tag")
        widgets = {
            "text": forms.TextInput(attrs={"placeholder": "Task"}),
            "tag": forms.TextInput(attrs={"placeholder": "field or focus"}),
        }