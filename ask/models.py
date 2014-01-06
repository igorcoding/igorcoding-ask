import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from djangosphinx.models import SphinxSearch
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    rating = models.IntegerField()

    def __unicode__(self):
        return '%s\'s profile' % self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance, rating=0)

post_save.connect(create_user_profile, sender=User)


class Tag(models.Model):
    tagname = models.CharField(max_length=50)

    class Meta:
        app_label = 'ask'

    def __unicode__(self):
        return unicode(self.tagname)


class QuestionVote(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey('Question')
    value = models.IntegerField(max_length=5)

    def __unicode__(self):
        return u"Q: " + unicode(self.question) + u" U: " + unicode(self.user) + u" value: " + unicode(self.value)


class AnswerVote(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey('Answer')
    value = models.IntegerField(max_length=5)

    def __unicode__(self):
        return u"A: " + unicode(self.answer) + u" U: " + unicode(self.user) + u" value: " + unicode(self.value)


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
            'contents': 50,
        }
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = timezone.now()
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
        if not self.id:
            self.date = timezone.now()
        return super(Answer, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s...' % self.contents[:30]

    class Meta:
        app_label = 'ask'





