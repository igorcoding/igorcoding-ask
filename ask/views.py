import json
import urllib2
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from ask.forms import *
from basicscripts import *
from math import ceil


def get_page(request):
    try:
        page = request.GET.get('page')
        if page is None:
            page = 1
        page = int(page)
        if page <= 0:
            raise Http404
        return page
    except:
        raise Http404


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


def get_ask_form(request):
    askform_error = False
    if request.method == "POST" and 'form_type' in request.POST and request.POST['form_type'] == 'ask':
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        form = AskForm(request.POST)
        if form.is_valid():
            author = request.user
            title = form.cleaned_data['title']
            contents = form.cleaned_data['contents']
            creation_date = datetime.datetime.today()
            tags = form.cleaned_data['tags']

            new_q = Question(author=author, title=title, contents=contents, creation_date=creation_date, rating=0)
            new_q.save()
            for tag in tags:
                if tag:
                    new_q.tag.add(get_or_add_tag(tag))
            new_q.save()
            new_q.author.userprofile.rating += 1
            new_q.author.userprofile.save()

            return HttpResponseRedirect("/question/" + str(new_q.id))
        else:
            askform_error = True
    else:
        form = AskForm()
    return form, askform_error


def get_response(request, required_page, extra_context, current_page):
    askform_error = False
    if request.method == "POST" and 'form_type' in request.POST and request.POST['form_type'] == 'ask':
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        form = AskForm(request.POST)
        if form.is_valid():
            author = request.user
            title = form.cleaned_data['title']
            contents = form.cleaned_data['contents']
            creation_date = datetime.datetime.today()
            tags = form.cleaned_data['tags']

            new_q = Question(author=author, title=title, contents=contents, creation_date=creation_date, rating=0)
            new_q.save()
            for tag in tags:
                if tag:
                    new_q.tag.add(get_or_add_tag(tag))
            new_q.save()
            new_q.author.userprofile.rating += 1
            new_q.author.userprofile.save()

            send_new_question(new_q)
            return HttpResponseRedirect("/question/" + str(new_q.id))
        else:
            askform_error = True
    else:
        form = AskForm()

    if 'total_count' not in extra_context:
        raise Exception
    count = extra_context['total_count']

    if not 'delim' in extra_context:
        extra_context['delim'] = '?'

    if 'objs_per_page' not in extra_context:
        objs_per_page = 20
    else:
        objs_per_page = extra_context['objs_per_page']

    pages_count = int(ceil(count / objs_per_page + 1))
    page_left, page_right = get_pages_bounds(pages_count, current_page)
    pages = range(page_left, page_right + 1)
    all_tags = get_all_tags()

    d = {'pages': pages,
         'pages_count': pages_count,
         'current_page': current_page,
         'all_tags': all_tags,
         'required_page': required_page,
         'ask_form': form,
         'askform_error': askform_error
    }

    return render(request, "index.html", dict(extra_context, **d))


def questions(request, tab):
    if not tab and tab is not None:
        tab = 'new'

    current_page = get_page(request)
    c = {}
    if tab is not None:
        if tab == 'new':
            c['res'] = get_questions_by_date(current_page)
            c['title'] = 'New Questions'
        elif tab == 'popular':
            c['res'] = get_questions_by_rating(current_page)
            c['title'] = 'Popular Questions'
        else:
            raise Http404

    c['page'] = '/questions/' + tab
    c['tab'] = tab
    c['total_count'] = Question.objects.count()
    return get_response(request, 'questions', c, current_page)


def new_questions(request):
    return questions(request, 'new')


def popular_questions(request):
    return questions(request, 'popular')


def deprecated(func):
    def new_func(request, tab):
        raise Http404
    return new_func


@deprecated
def answers(request, tab):
    if not tab and tab is not None:
        tab = 'new'

    current_page = get_page(request)
    c = {}
    if tab is not None:
        if tab == 'new':
            c['res'] = get_answers_by_date(current_page)
            c['title'] = 'New Answers'
        elif tab == 'popular':
            c['res'] = get_answers_by_rating(current_page)
            c['title'] = 'Popular Answers'
        else:
            raise Http404
    c['page'] = '/answers/' + tab
    c['tab'] = tab
    c['total_count'] = Answer.objects.count()
    return get_response(request, 'answers', c, current_page)


def new_answers(request):
    return answers(request, 'new')


def popular_answers(request):
    return answers(request, 'popular')


@login_required
def users(request):
    current_page = get_page(request)

    order = request.GET.get('order')
    if order is None:
        order = 'date'

    try:
        all_users = get_all_users(order, current_page)
        if all_users is None:
            raise Http404

        c = {}
        c['title'] = 'All users'
        c['res'] = all_users
        c['tab'] = order
        c['page'] = '/users?order=%s' % (order, )
        c['total_count'] = User.objects.count()
        c['delim'] = '&'
        return get_response(request, 'users', c, current_page)
    except:
        raise Http404


def question_page(request, q_id):
    q = get_question(q_id)
    answerform_error = False
    if request.method == 'POST' and 'form_type' in request.POST and request.POST['form_type'] == 'answer':
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            contents = answer_form.cleaned_data['contents']
            ans = Answer(question=q, author=request.user, date=datetime.datetime.today(), correct=False, rating=0,
                         contents=contents)
            ans.save()
            return HttpResponseRedirect('/question/' + str(q_id) + '/' + '#answer_' + str(ans.id))
        else:
            answerform_error = True
    else:
        answer_form = AnswerForm()

    try:
        current_page = get_page(request)
        c = {'q': q,
             'answers': get_answers_for_question(q_id),
             'title': q.title,
             'page': '/question/' + str(q_id),
             'answer_form': answer_form,
             'answerform_error': answerform_error,
             'total_count': q.answer_set.count(),
             'objs_per_page': 30}
    except:
        raise Http404

    return get_response(request, 'question', c, current_page)


@login_required
def user(request, username, tab=None):
    if not tab:
        tab = 'questions'
    try:
        user = get_user_by_name(username)
    except:
        raise Http404

    page = get_page(request)

    if tab == "questions":
        res = get_questions_by_user(user, page)
        total_count = Question.objects.filter(author_id=user.id).count()
    elif tab == "answers":
        res = get_answers_by_user(user, page)
        total_count = Answer.objects.filter(author_id=user.id).count()
    else:
        raise Http404

    c = {'show_user': user,
         'res': res,
         'tab': tab,
         'page': '/users/' + user.username + '/' + tab,
         'title': '%s\'s %s' % (user.username, tab),
         'total_count': total_count,
         'delim': '?'}

    return get_response(request, 'user', c, page)


def tag_search(request, tagname, tab):
    if tagname is None or not tagname:
        raise Http404

    if not tab and tab is not None:
        tab = 'new'

    current_page = get_page(request)
    c = {}
    try:
        if tab == 'new':
            c['res'] = get_questions_by_tag(tagname, current_page)
        elif tab == 'popular':
            c['res'] = get_questions_by_tag(tagname, current_page, order='rating')
        else:
            raise Http404
    except:
        raise Http404

    c['page'] = '/tag/' + tagname + '/' + tab
    c['tab'] = tab
    c['search_tag'] = get_tag(tagname)
    c['tagname'] = tagname
    c['title'] = 'Search tag: '
    c['extra_title'] = tagname
    c['show_title'] = True
    c['total_count'] = get_tag(tagname).question_set.count()
    return get_response(request, 'tag/' + tagname, c, current_page)


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

        value = 0
        if way == 'up':
            value = 1
        elif way == 'down':
            value = -1

        if request.user.is_authenticated():
            ok = False
            if content_type == 'question':
                ok = change_q_rating(content, request.user, value)
            elif content_type == 'answer':
                ok = change_a_rating(content, request.user, value)

            if ok is None:
                response_data = {'msg': 'You cannot vote to your own %s.' % (content_type, ),
                                 'notify': 'warning',
                                 'rating': content.rating,
                                 'user_rating': request.user.userprofile.rating}
            else:
                if ok:
                    content.rating += value
                    content.save()

                    response_data = {
                        'msg': "Your vote accepted.",
                        'notify': 'success',
                        'rating': content.rating,
                        'user_rating': content.author.userprofile.rating
                    }
                else:
                    response_data = {
                        'msg': "You have already voted this way.\nYou cannot do it twice.",
                        'notify': 'danger',
                        'rating': content.rating
                    }
        else:
            response_data = {
                'msg': "You have to be logged in to make a vote.",
                'notify': 'danger',
                'rating': content.rating
            }
    else:
        response_data = {
            'msg': error,
            'notify': 'danger',
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def set_correct(request):
    try:
        a_id = int(request.POST['answer_id'])
        answer = get_answer(a_id)

        if answer.question.author == request.user:
            if not answer.correct:
                answer.correct = True
                response_data = {
                    'msg': "Answer marked as correct."
                }
            else:
                answer.correct = False
                response_data = {
                    'msg': "Answer is no longer correct."
                }
            answer.save()
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        raise Http404


def my_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    c = {'tags': get_top_tags(30),
         'new_users': get_users(10),
         'ask_form': AskForm(),
         'title': 'Login'
    }
    return django_login(request, extra_context=c)


def my_logout(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    c = {'title': 'Logging out...'}
    return django_logout(request, extra_context=c, next_page='/')


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST, request.FILES)
        if reg_form.is_valid():
            if 'user_pic' in request.FILES:
                save_userpic(request.FILES['user_pic'], request.POST['username'])
            new_user = reg_form.save()
            new_user = authenticate(username=request.POST['username'], password=request.POST['password2'])
            login(request, new_user)

            try:
                redirect_to = request.GET['next']
            except:
                raise Http404
            return HttpResponseRedirect(redirect_to)
    else:
        reg_form = RegistrationForm()

    return render(request, "registration/register.html", {
        'reg_form': reg_form,
        'ask_form': AskForm(),
        'tags': get_top_tags(30),
        'new_users': get_users(10),
        'title': 'Sign up'
    })


def search(request, tab):
    if not tab or tab is None:
        tab = 'questions'
    query = request.GET.get('query')
    current_page = get_page(request)
    if query is None:
        raise Http404

    c = {}
    if tab == 'questions':
        c['res'] = search_questions(query, current_page)
        c['total_count'] = Question.search.query(query).count()
    elif tab == 'answers':
        c['res'] = search_answers(query, current_page)
        c['total_count'] = Answer.search.query(query).count()
    else:
        raise Http404

    c['search'] = True
    c['page'] = '/search/%s?query=%s' % (tab, query)
    c['delim'] = '&'
    c['tab'] = tab
    c['title'] = 'Search: %s' % query
    c['show_title'] = True
    c['base_url'] = '/search'
    c['query'] = query

    return get_response(request, tab, c, current_page)
