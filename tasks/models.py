from django.conf import settings
from django.db import models
from django.urls import reverse


<<<<<<< HEAD
class TaskList(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_lists")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="shared_lists", blank=True)
=======
class TaskGroup(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_groups",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="task_groups",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
>>>>>>> task-groups

    def __str__(self):
        return self.name


class task(models.Model):
    text = models.CharField(max_length=140)
    tag = models.CharField(max_length=20)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    viewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="shared_tasks",
        blank=True,
    )
    group = models.ForeignKey(
        TaskGroup,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks",
    )

    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)

    def __str__(self):
        return self.text
