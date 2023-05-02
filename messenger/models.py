import datetime
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default=None, blank=True, null=True)

    @property
    def user_avatar(self):
        img = self.avatar
        return '/static/no_avatar.jpg' if not img.name else f'/media/{img}'

    def __str__(self):
        return self.user.username


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_message')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receive_message')
    created = models.DateTimeField(auto_now_add=True)
    read = models.DateTimeField(default=None, blank=True, null=True)
    text = models.TextField()

    def make_read(self):
        if not self.read:
            self.read = datetime.datetime.now()
            self.save()

    @classmethod
    def total(cls, sender, receiver):
        return cls.objects.filter(sender=sender, receiver=receiver).count()

    @classmethod
    def unread(cls, sender, receiver):
        return cls.objects.filter(sender=sender, receiver=receiver, read__isnull=True).count()
