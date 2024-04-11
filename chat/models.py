from django.db import models
from project.models import Project
from project.models import User


# Create your models here.

class ChatMassage(models.Model):
    MSG_TYPE_CHOICES = (
        (1, 'Text'),
        (2, 'File'),
        (3, 'Image'),
        (4, 'Quote')
    )
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.PROTECT)
    talker = models.ForeignKey(Project, on_delete=models.PROTECT)
    msg_type = models.IntegerField(choices=MSG_TYPE_CHOICES)
    quote = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)


class UserLastRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    last_time = models.DateTimeField(auto_now=True)
    talker = models.ForeignKey(Project, on_delete=models.PROTECT)
