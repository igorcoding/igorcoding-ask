# coding=utf8
import random
import sys, os
from twisted.python._reflectpy3 import ObjectNotFound
from django.core.exceptions import ObjectDoesNotExist
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


def get_answer(answer_id):
    return Answer.objects.get(pk=answer_id)


def get_answers_for_question(question_id):
    return Answer.objects.filter(question=get_question(question_id)).order_by('-date').order_by('-rating')


def get_answers_by_date(page, count=30):
    offset = (page - 1) * count
    return Answer.objects.order_by('-date')[offset:(offset + count)]


def get_answers_by_rating(page, count=30):
    offset = (page - 1) * count
    return Answer.objects.order_by('-rating')[offset:(offset + count)]


def get_questions_by_user(user, page, count=30):
    offset = (page - 1) * count
    return Question.objects.filter(author_id=user.id).order_by('-creation_date')[offset:(offset + count)]


def get_answers_by_user(user, page, count=30):
    offset = (page - 1) * count
    return Answer.objects.filter(author_id=user.id).order_by('-date')[offset:(offset + count)]


def get_or_add_tag(tagname):
    try:
        tag = Tag.objects.get(tagname=tagname)
    except ObjectDoesNotExist:
        tag = Tag(tagname=tagname)
        tag.save()
    return tag


def get_tag(tagname):
    return Tag.objects.get(tagname=tagname)


def get_questions_by_tag(tagname, page, count=30, order='date'):
    offset = (page - 1) * count
    if order == 'date':
        return get_tag(tagname).question_set.order_by('-creation_date')[offset:(offset + count)]
    elif order == 'rating':
        return get_tag(tagname).question_set.order_by('-rating')[offset:(offset + count)]
    else:
        raise Exception


def get_all_tags():
    return Tag.objects.all()


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
    return User.objects.filter(pk=user_id)[0]


def get_user_by_name(username):
    return User.objects.filter(username=username)[0]


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


def get_question_rating(question_id):
    return QuestionVote.objects.filter(question_id=question_id).aggregate(sum=models.Sum('value'))['sum']


def get_answer_rating(answer_id):
    return AnswerVote.objects.filter(answer_id=answer_id).aggregate(sum=models.Sum('value'))['sum']


def increase_q_rating(q, user):
    qvote = QuestionVote(question=q, user=user, value=1)
    qvote.save()
    q.rating = get_question_rating(q.id)
    q.save()


def decrease_q_rating(q, user):
    qvote = QuestionVote(question=q, user=user, value=-1)
    qvote.save()
    q.rating = get_question_rating(q.id)
    q.save()


def increase_a_rating(a, user):
    avote = AnswerVote(answer=a, user=user, value=1)
    avote.save()
    a.rating = get_answer_rating(a.id)
    a.save()


def decrease_a_rating(a, user):
    avote = AnswerVote(answer=a, user=user, value=-1)
    avote.save()
    a.rating = get_answer_rating(a.id)
    a.save()


def change_q_rating(q, user, way):
    if way == 'up':
        increase_q_rating(q, user)
    elif way == 'down':
        decrease_q_rating(q, user)


def change_a_rating(a, user, way):
    if way == 'up':
        increase_a_rating(a, user)
    elif way == 'down':
        decrease_a_rating(a, user)