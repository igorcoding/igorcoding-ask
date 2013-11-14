# Create your views here.
from datetime import datetime
from django.template import loader, Context
from django.http import HttpResponse
from ask.models import *
from basicscripts import *
from math import ceil


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


def new_questions(request, page=None):
    if page is None:
        page = request.GET.get('page')
        if page is None:
            page = 1
        page = int(page)

    qs = get_questions_by_date(page)
    tags = get_top_tags(30)
    new_users = get_users(10)

    pages_count = Question.objects.count() / 30 + 1
    page_left, page_right = get_pages_bounds(pages_count, page)

    pages = range(page_left, page_right + 1)

    t = loader.get_template("index.html")
    c = Context({'questions': qs,
                 'tags': tags,
                 'new_users': new_users,
                 'new': True,
                 'pages': pages,
                 'pages_count': pages_count,
                 'page': '',
                 'current_page': page})
    return HttpResponse(t.render(c), mimetype='text/html')


def popular_questions(request, page=None):
    if page is None:
        page = request.GET.get('page')
        if page is None:
            page = 1
        page = int(page)

    qs = get_questions_by_rating(page)
    tags = get_top_tags(30)
    new_users = get_users(10)

    pages_count = ceil(Question.objects.count() / 30)
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
    return HttpResponse(t.render(c), mimetype='text/html')