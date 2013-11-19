# Create your views here.
from datetime import datetime
import json
from django.shortcuts import render
from django.template import loader, Context, RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from ask.forms import AskForm
from ask.models import *
from basicscripts import *
from math import ceil
from django.views.decorators.csrf import ensure_csrf_cookie


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

    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/thanks")
    else:
        form = AskForm()
    page = get_page(request)
    qs = get_questions_by_date(page)

    tags = get_top_tags(30)
    new_users = get_users(10)
    pages_count = int(ceil(Question.objects.count() / 30 + 1))
    page_left, page_right = get_pages_bounds(pages_count, page)
    pages = range(page_left, page_right + 1)
    all_tags = get_all_tags()

    c = {'questions': qs,
         'tags': tags,
         'new_users': new_users,
         'pages': pages,
         'pages_count': pages_count,
         'page': '',
         'current_page': page,
         'all_tags': all_tags,
         'required_content': 'questions',
         'form': form}
    return render(request, "index.html", c)


def popular_questions(request):
    page = get_page(request)
    qs = get_questions_by_rating(page)

    tags = get_top_tags(30)
    new_users = get_users(10)
    pages_count = int(ceil(Question.objects.count() / 30 + 1))
    page_left, page_right = get_pages_bounds(pages_count, page)
    pages = range(page_left, page_right + 1)

    c = {'questions': qs,
         'tags': tags,
         'new_users': new_users,
         'pages': pages,
         'pages_count': pages_count,
         'page': 'popular',
         'current_page': page,
         'required_content': 'questions'}
    return render(request, "index.html", c)


def new_answers(request):
    page = get_page(request)
    answers = get_answers_by_date(page)

    tags = get_top_tags(30)
    new_users = get_users(10)
    pages_count = int(ceil(Answer.objects.count() / 30 + 1))
    page_left, page_right = get_pages_bounds(pages_count, page)
    pages = range(page_left, page_right + 1)

    c = {'answers': answers,
         'tags': tags,
         'new_users': new_users,
         'pages': pages,
         'pages_count': pages_count,
         'page': 'answers',
         'current_page': page,
         'required_content': 'answers'}
    return render(request, "index.html", c)


def popular_answers(request):
    page = get_page(request)
    answers = get_answers_by_rating(page)

    tags = get_top_tags(30)
    new_users = get_users(10)
    pages_count = int(ceil(Answer.objects.count() / 30 + 1))
    page_left, page_right = get_pages_bounds(pages_count, page)
    pages = range(page_left, page_right + 1)

    c = {'answers': answers,
         'tags': tags,
         'new_users': new_users,
         'pages': pages,
         'pages_count': pages_count,
         'page': 'popular',
         'current_page': page,
         'required_content': 'answers'}
    return render(request, "index.html", c)


def users(request):
    return None


def question_page(request):
    try:
        q_id = int(request.GET['q'])
    except MultiValueDictKeyError:
        raise Http404

    page = get_page(request)
    q = get_question(q_id)
    answers = get_answers_for_question(q_id)

    tags = get_top_tags(30)
    new_users = get_users(10)
    pages_count = int(ceil(q.answer_set.count() / 30 + 1))
    page_left, page_right = get_pages_bounds(pages_count, page)
    pages = range(page_left, page_right + 1)

    c = {'q': q,
         'answers': answers,
         'tags': tags,
         'new_users': new_users,
         'pages': pages,
         'pages_count': pages_count,
         'page': '',
         'current_page': page,
         'required_content': 'question'}
    return render(request, "index.html", c)


def user(request):
    try:
        username = request.GET['username']

    except MultiValueDictKeyError:
        raise Http404

    tab = request.GET['tab'] if 'tab' in request.GET else 'questions'
    try:
        user = get_user_by_name(username)
    except:
        raise Http404

    page = get_page(request)

    if tab == "questions":
        res = get_questions_by_user(user, page)
    elif tab == "answers":
        res = get_answers_by_user(user, page)
    else:
        raise Http404

    tags = get_top_tags(30)
    new_users = get_users(10)
    pages_count = int(ceil(res.count() / 30 + 1))
    page_left, page_right = get_pages_bounds(pages_count, page)
    pages = range(page_left, page_right + 1)

    c = {'user': user,
         'tab': tab,
         'tags': tags,
         'new_users': new_users,
         'pages': pages,
         'pages_count': pages_count,
         'page': 'user/?username=' + user.username + '&tab=' + tab,
         'current_page': page,
         'required_content': 'user'}

    if tab == "questions":
        c["questions"] = res
    elif tab == "answers":
        c["answers"] = res

    return render(request, "index.html", c)


def change_question_rating(request):
    try:
        q_id = int(request.POST['q'])
        way = request.POST['way']
        user_id = int(request.POST['user_id'])
    except MultiValueDictKeyError:
        raise Http404
    if way == "increase":
        increase_q_rating(q_id, user_id)
    elif way == "decrease":
        decrease_q_rating(q_id, user_id)

    response_data = {
        'msg': "Your vote accepted.",
        'rating': get_question(q_id).rating
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def change_answer_rating(request):
    try:
        a_id = int(request.POST['a'])
        way = request.POST['way']
        user_id = int(request.POST['user_id'])
    except MultiValueDictKeyError:
        raise Http404
    if way == "increase":
        increase_a_rating(a_id, user_id)
    elif way == "decrease":
        decrease_a_rating(a_id, user_id)

    response_data = {
        'msg': "Your vote accepted.",
        'rating': get_answer(a_id).rating
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def set_correct(request):
    try:
        a_id = int(request.POST['answer_id'])
    except MultiValueDictKeyError:
        raise Http404

    answer = get_answer(a_id)
    answer.correct = True
    answer.save()
    response_data = {
        'msg': "Answer marked as correct."
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")