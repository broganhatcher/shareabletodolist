from django.conf import settings
from django.db import models
from django.urls import reverse

class task(models.Model):
    text = models.CharField(max_length=140)
    tag = models.CharField(max_length=20)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.text