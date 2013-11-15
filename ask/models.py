from gtk.keysyms import question
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Tag(models.Model):
    tagname = models.CharField(max_length=50)

    class Meta:
        app_label = 'ask'


class Question(models.Model):
    title = models.CharField(max_length=255)
    contents = models.TextField()
    author = models.ForeignKey(User)
    creation_date = models.DateTimeField()
    tag = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)
    #raters = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.creation_date = datetime.datetime.today()
        return super(Question, self).save(*args, **kwargs)

    class Meta:
        app_label = 'ask'


class Answer(models.Model):
    contents = models.TextField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    date = models.DateTimeField()
    correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    #raters = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.date = datetime.datetime.today()
        return super(Answer, self).save(*args, **kwargs)

    class Meta:
        app_label = 'ask'





