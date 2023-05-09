from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def get_url(self):
        return f'/ws/chat/{self.pk}'

    @property
    def get_room_url(self):
        return reverse('chat.room', kwargs={'pk': self.pk}) if self.pk else ''

