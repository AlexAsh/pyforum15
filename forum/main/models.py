import re
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, null=True, default=None)

    def __str__(self):
        return self.text


class Comment(MPTTModel):
    text = models.TextField()
    user = models.ForeignKey(User, null=True, default=None)
    created = models.DateTimeField(default=datetime.now, blank=True)
    parent = TreeForeignKey("self", null=True, blank=True, related_name="children", db_index=True)

    class MPTTMeta:
        order_insertion_by = ["created"]

    @staticmethod
    def get_comment_by_id_string(id_string):
        if not re.match("^[1-9][0-9]*$", id_string):
            return None

        try:
            comment = Comment.objects.get(pk=int(id_string.strip()))
        except Comment.DoesNotExist:
            return None
        else:
            return comment

    def __str__(self):
        return self.text
