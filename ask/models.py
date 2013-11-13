from gtk.keysyms import question
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Tag(models.Model):
    tagname = models.CharField(max_length=50)

    class Meta:
        app_label = 'ask'


class Question(models.Model):
    title = models.CharField(max_length=255)
    contents = models.CharField(max_length=1500)
    author = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag)
    rating = models.IntegerField()

    class Meta:
        app_label = 'ask'


class Answer(models.Model):
    contents = models.CharField(max_length=1500)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    correct = models.BooleanField(default=False)
    rating = models.IntegerField()

    class Meta:
        app_label = 'ask'





