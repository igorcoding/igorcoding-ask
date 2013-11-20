# Create your views here.
from datetime import datetime
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
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


def get_count(to_count):
    return to_count.count()


def get_response(request, required_page, tab=None):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/thanks")
    else:
        form = AskForm()

    page = get_page(request)

    if not tab and tab is not None:
        tab = 'new'
    c = {}
    if required_page == 'questions':
        if tab is not None:
            if tab == 'new':
                c['res'] = get_questions_by_date(page)
            elif tab == 'popular':
                c['res'] = get_questions_by_rating(page)
            else:
                raise Http404
        to_count = Question.objects

    elif required_page == 'answers':
        if tab is not None:
            if tab == 'new':
                c['res'] = get_answers_by_date(page)
            elif tab == 'popular':
                c['res'] = get_answers_by_rating(page)
            else:
                raise Http404
        to_count = Answer.objects

    elif required_page == 'question':
        try:
            q_id = int(request.GET['q'])
        except MultiValueDictKeyError:
            raise Http404

        c['q'] = get_question(q_id)
        c['answers'] = get_answers_for_question(q_id)
        to_count = c['q'].answer_set

    else:
        raise Http404

    tags = get_top_tags(30)
    new_users = get_users(10)
    pages_count = int(ceil(get_count(to_count) / 30 + 1))
    page_left, page_right = get_pages_bounds(pages_count, page)
    pages = range(page_left, page_right + 1)
    all_tags = get_all_tags()

    d = {'tags': tags,
         'new_users': new_users,
         'pages': pages,
         'pages_count': pages_count,
         'tab': tab,
         'current_page': page,
         'all_tags': all_tags,
         'required_page': required_page,
         'form': form
         }
    return render(request, "index.html", dict(c, **d))


def new_questions(request):
    return get_response(request, 'questions', 'new')


def popular_questions(request):
    return get_response(request, 'questions', 'popular')


def new_answers(request):
    return get_response(request, 'answers', 'new')


def popular_answers(request):
    return get_response(request, 'answers', 'popular')


def users(request):
    return None


def question_page(request):
    return get_response(request, 'question')


@login_required
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

    c = {'show_user': user,
         'res': res,
         'tab': tab,
         'tags': tags,
         'new_users': new_users,
         'pages': pages,
         'pages_count': pages_count,
         'page': 'user/?username=' + user.username + '&tab=' + tab,
         'current_page': page,
         'required_page': 'user'}

    return render(request, "index.html", c)


@login_required
def user1(request, username, tab=None):
    if not tab:
        tab = 'questions'
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

    c = {'show_user': user,
         'res': res,
         'tab': tab,
         'tags': tags,
         'new_users': new_users,
         'pages': pages,
         'pages_count': pages_count,
         'page': 'user/?username=' + user.username + '&tab=' + tab,
         'current_page': page,
         'required_page': 'user'}

    return render(request, "index.html", c)


def change_content_rating(request, content_type, way):
    try:
        content_id = int(request.POST['content_id'])
    except MultiValueDictKeyError:
        raise Http404
    error = None

    if error is None:
        if content_type == 'question':
            content = get_question(content_id)
        elif content_type == 'answer':
            content = get_answer(content_id)
        else:
            raise Http404

        if request.user.is_authenticated():
            if content_type == 'question':
                change_q_rating(content, request.user, way)
            elif content_type == 'answer':
                change_a_rating(content, request.user, way)

            response_data = {
                'msg': "Your vote accepted.",
                'rating': content.rating
            }
        else:
            response_data = {
                'msg': "You should login to make a vote.",
                'rating': content.rating
            }
    else:
        response_data = {
            'msg': error
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