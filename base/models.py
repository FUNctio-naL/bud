from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # can be null and blank
    participant = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True) # record timestamp, everytime it is updated
    created = models.DateTimeField(auto_now_add=True) # record timestamp, only once (when it is created)

    class Meta:
        ordering  = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 1toMany
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) # record timestamp, everytime it is updated
    created = models.DateTimeField(auto_now_add=True) # record timestamp, only once (when it is created)
    class Meta:
        ordering  = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50] # Only first 50 chars viewing from outside.
