from django.db import models

from apps.common import enums
from apps.users.models import User


# Create your models here.
class Chats(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(null=True, blank=True)
    sender = models.CharField(choices=enums.ChatSenderType.choices)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chat.name

    class Meta:
        ordering = ['created_at']


class ChatFile(models.Model):
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='chat_files')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chat.name
