from gtk.keysyms import question
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from djangosphinx.models import SphinxSearch


class Tag(models.Model):
    tagname = models.CharField(max_length=50)

    class Meta:
        app_label = 'ask'


class QuestionVote(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey('Question')
    value = models.IntegerField(max_length=5)


class AnswerVote(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey('Answer')
    value = models.IntegerField(max_length=5)


class Question(models.Model):
    title = models.CharField(max_length=255)
    contents = models.TextField()
    author = models.ForeignKey(User)
    creation_date = models.DateTimeField()
    tag = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)

    search = SphinxSearch(
        index='questions_index',
        weights={
            'title': 100,
            'contents': 100,
        }
    )

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.creation_date = datetime.datetime.today()
        return super(Question, self).save(*args, **kwargs)

    class Meta:
        app_label = 'ask'

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    contents = models.TextField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    date = models.DateTimeField()
    correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)

    search = SphinxSearch(
        index='answers_index',
        weights={
            'contents': 100,
        }
    )

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.date = datetime.datetime.today()
        return super(Answer, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s...' % self.contents[:30]

    class Meta:
        app_label = 'ask'





