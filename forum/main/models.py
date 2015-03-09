from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, null=True, default=None)

    def __str__(self):
        return self.text
