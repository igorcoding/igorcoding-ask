# coding=utf8
import json
import random
import sys, os
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.core.serializers import json as django_json
from django.db.models import Q, F
import memcache


sys.path.append('/home/igor/Documents/www/igorcoding_ask/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'igorcoding_ask.settings'
from django.conf import settings
from models import *
from django.contrib.auth.models import User
from pprint import pprint


def get_questions_by_date(page, count=20):
    offset = (page - 1) * count
    return Question.objects.order_by('-creation_date')[offset:(offset + count)]


def get_questions_by_rating(page, count=20):
    offset = (page - 1) * count
    return Question.objects.order_by('-rating')[offset:(offset + count)]


def get_question(question_id):
    return Question.objects.get(pk=question_id)


def get_answer(answer_id):
    return Answer.objects.get(pk=answer_id)


def get_answers_for_question(question_id):
    return Answer.objects.filter(question=get_question(question_id)).order_by('-date').order_by('-rating')


def get_answers_by_date(page, count=20):
    offset = (page - 1) * count
    return Answer.objects.order_by('-date')[offset:(offset + count)]


def get_answers_by_rating(page, count=20):
    offset = (page - 1) * count
    return Answer.objects.order_by('-rating')[offset:(offset + count)]


def get_questions_by_user(user, page, count=20):
    offset = (page - 1) * count
    return Question.objects.filter(author_id=user.id).order_by('-creation_date')[offset:(offset + count)]


def get_answers_by_user(user, page, count=20):
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


def get_questions_by_tag(tagname, page, count=20, order='date'):
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
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    #mc.delete('top_tags')
    top = mc.get('top_tags')
    if not top:
        res = []
        try:
            weights_count = 5
            tags = Tag.objects.all().annotate(questions_count=models.Count('question')).order_by('-questions_count')[:count]
            max_value = tags[0].questions_count
            min_value = tags[count - 1].questions_count
            delta = (max_value - min_value) / weights_count

            weight = weights_count
            prev_count = tags[0].questions_count
            for tag in tags:
                if prev_count - tag.questions_count > delta:
                    weight -= 1
                    prev_count = tag.questions_count
                res.append({'tagname': tag.tagname, 'weight': weight})

            random.shuffle(res)
        except:
            res = []
        mc.set('top_tags', json.dumps(res, ensure_ascii=False), time=4*24*60*60)
        return res
    res = json.loads(top, encoding='utf-8')
    return res


def get_user(user_id):
    return User.objects.filter(pk=user_id)[0]


def get_user_by_name(username):
    return User.objects.filter(username=username)[0]


def get_all_users(order, page, count=20):
    offset = (page - 1) * count
    if order == 'date':
        return User.objects.order_by('-date_joined').filter(~Q(pk=1))[offset:(offset + count)]
    elif order == 'rating':
        return User.objects.order_by('-userprofile__rating').filter(~Q(pk=1))[offset:(offset + count)]
    elif order == 'username':
        return User.objects.order_by('username').filter(~Q(pk=1))[offset:(offset + count)]
    elif order == 'name':
        return User.objects.order_by('last_name').order_by('first_name').filter(~Q(pk=1))[offset:(offset + count)]
    else:
        return None


def get_users(count=None):
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    #mc.delete('new_users')
    jsonSer = django_json.Serializer()
    new_users = mc.get('new_users')
    if new_users is None:
        try:
            if count is None:
                new_users = User.objects.filter(~Q(pk=1)).order_by('-date_joined')
            else:
                new_users = User.objects.filter(~Q(pk=1)).order_by('-date_joined')[:count + 1]
        except:
            new_users = []
        mc.set('new_users', jsonSer.serialize(new_users), time=5*60)
        return new_users
    res = [obj.object for obj in django_json.Deserializer(new_users)]
    return res


def get_question_rating(question_id):
    return QuestionVote.objects.filter(question_id=question_id).aggregate(sum=models.Sum('value'))['sum']


def get_answer_rating(answer_id):
    return AnswerVote.objects.filter(answer_id=answer_id).aggregate(sum=models.Sum('value'))['sum']


def change_q_rating(q, user, value):
    ok = False
    if user == q.author:
        return None
    try:
        vote_entry = QuestionVote.objects.get(user=user, question=q)
        if vote_entry.value != value:
            q.rating += -vote_entry.value
            vote_entry.delete()
            if value == 1:
                q.author.userprofile.rating += 2
            elif value == -1:
                q.author.userprofile.rating -= 3
            ok = True
    except QuestionVote.DoesNotExist:
        ok = True

    if ok:
        vote_entry = QuestionVote(user=user, question=q, value=value)
        vote_entry.save()
        if value == 1:
            q.author.userprofile.rating += 3
        elif value == -1:
            q.author.userprofile.rating -= 2
        q.author.userprofile.save()
    return ok


def change_a_rating(a, user, value):
    ok = False
    if user == a.author:
        return None
    try:
        vote_entry = AnswerVote.objects.get(user=user, answer=a)
        if vote_entry.value != value:
            a.rating += -vote_entry.value
            vote_entry.delete()
            if value == 1:
                a.author.userprofile.rating += 2
            elif value == -1:
                a.author.userprofile.rating -= 5
            ok = True
    except AnswerVote.DoesNotExist:
        ok = True

    if ok:
        vote_entry = AnswerVote(user=user, answer=a, value=value)
        vote_entry.save()
        if value == 1:
            a.author.userprofile.rating += 5
        elif value == -1:
            a.author.userprofile.rating -= 2
        a.author.userprofile.save()
    return ok


def save_userpic(f, username):
    filename = '%s/%s.jpg' % (settings.MEDIA_ROOT, username)
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def search_questions(query, page, count=20):
    offset = (page - 1) * count
    return Question.search.query(query).order_by('@weight')[offset:(offset + count)]


def search_answers(query, page, count=20):
    offset = (page - 1) * count
    return Answer.search.query(query)[offset:(offset + count)]
