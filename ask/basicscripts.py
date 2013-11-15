# coding=utf8
import random
import sys, os
from django.db.models import Q

sys.path.append('/home/igor/Documents/www/igorcoding_ask/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'igorcoding_ask.settings'
from django.conf import settings
from models import *
from django.contrib.auth.models import User
from pprint import pprint


def get_questions_by_date(page, count=30):
    offset = (page - 1) * count
    return Question.objects.order_by('-creation_date')[offset:(offset + count)]


def get_questions_by_rating(page, count=30):
    offset = (page - 1) * count
    return Question.objects.order_by('-rating')[offset:(offset + count)]


def get_question(question_id):
    return Question.objects.get(pk=question_id)


def get_answers(question_id):
    return Answer.objects.filter(question=get_question(question_id)).order_by('-date').order_by('-rating')


def get_tag(tag_id):
    return Tag.objects.get(pk=tag_id)


def get_questions_by_tag(tag_id, page, count=30):
    offset = (page - 1) * count
    return get_tag(tag_id).question_set.order_by('-creation_date')[offset:(offset + count)]


def get_top_tags(count):
    weights_count = 5
    tags = Tag.objects.all().annotate(questions_count=models.Count('question')).order_by('-questions_count')[:count]
    max_value = tags[0].questions_count
    min_value = tags[count - 1].questions_count
    delta = (max_value - min_value) / weights_count

    res = []
    weight = weights_count
    prev_count = tags[0].questions_count
    for tag in tags:
        if prev_count - tag.questions_count > delta:
            weight -= 1
            prev_count = tag.questions_count
        res.append({'tag': tag, 'weight': weight})

    random.shuffle(res)
    return res


def get_user(user_id):
    return User.objects.filter(pk=user_id)


def get_users(count=None, order='date_joined'):
    if order == 'date_joined':
        if count is None:
            return User.objects.order_by('-date_joined')
        return User.objects.order_by('-date_joined').filter(~Q(pk=1))[:count + 1]

    if order == 'rating':
        if count is None:
            return User.objects.order_by('-rating')
        return User.objects.order_by('-rating').filter(~Q(pk=1))[:count + 1]

    return None


def increase_q_rating(question_id):
    q = get_question(question_id)
    q.rating += 1
    q.save()


def decrease_question_rating(question_id):
    q = get_question(question_id)
    q.rating -= 1
    q.save()