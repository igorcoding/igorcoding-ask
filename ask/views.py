# Create your views here.
from datetime import datetime
import json
from django.template import loader, Context
from django.http import HttpResponse, Http404
from django.utils.datastructures import MultiValueDictKeyError
from ask.models import *
from basicscripts import *
from math import ceil


def get_page(request):
    page = request.GET.get('page')
    if page is None:
        page = 1
    return int(page)


def get_pages_bounds(pages_count, page):
    if page <= 5:
        page_left = 1
    else:
        page_left = page - 4

    if page < 5 and pages_count >= 10:
        page_right = 10
    elif page < pages_count - 5:
        page_right = page + 5
    else:
        page_right = pages_count
    return page_left, page_right


def new_questions(request):
    page = get_page(request)

    qs = get_questions_by_date(page)
    tags = get_top_tags(30)
    new_users = get_users(10)

    pages_count = int(ceil(Question.objects.count() / 30 + 1))
    page_left, page_right = get_pages_bounds(pages_count, page)

    pages = range(page_left, page_right + 1)

    t = loader.get_template("index.html")
    c = Context({'questions': qs,
                 'tags': tags,
                 'new_users': new_users,
                 'pages': pages,
                 'pages_count': pages_count,
                 'page': '',
                 'current_page': page})
    return HttpResponse(t.render(c))


def popular_questions(request):
    page = get_page(request)

    qs = get_questions_by_rating(page)
    tags = get_top_tags(30)
    new_users = get_users(10)

    pages_count = int(ceil(Question.objects.count() / 30 + 1))
    page_left, page_right = get_pages_bounds(pages_count, page)

    pages = range(page_left, page_right + 1)

    t = loader.get_template("index.html")
    c = Context({'questions': qs,
                 'tags': tags,
                 'new_users': new_users,
                 'pages': pages,
                 'pages_count': pages_count,
                 'page': 'popular',
                 'current_page': page})
    return HttpResponse(t.render(c))


def question_page(request):
    page = get_page(request)
    try:
        q_id = int(request.GET['q'])
    except MultiValueDictKeyError:
        raise Http404

    q = get_question(q_id)
    answers = get_answers(q_id)
    tags = get_top_tags(30)
    new_users = get_users(10)


    pages_count = int(ceil(q.answer_set.count() / 30 + 1))
    page_left, page_right = get_pages_bounds(pages_count, page)
    pages = range(page_left, page_right + 1)

    t = loader.get_template("question.html")

    c = Context({'q': q,
                 'answers': answers,
                 'tags': tags,
                 'new_users': new_users,
                 'pages': pages,
                 'pages_count': pages_count,
                 'current_page': page})
    return HttpResponse(t.render(c))


def change_question_rating(request):
    try:
        q_id = int(request.GET['q'])
        way = request.GET['way']
    except MultiValueDictKeyError:
        raise Http404
    if way == "increase":
        increase_q_rating(q_id)
    elif way == "decrease":
        decrease_question_rating(q_id)

    response_data = {
        'msg': "Your vote accepted.",
        'rating': get_question(q_id).rating
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def new_answers(request):
    pass


def popular_answers(request):
    return None


def users(request):
    return None


