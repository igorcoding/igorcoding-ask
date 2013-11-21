import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from ask.forms import *
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


def get_count(to_count):
    return to_count.count()


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

            return HttpResponseRedirect("/question/" + str(new_q.id))
        else:
            askform_error = True
    else:
        form = AskForm()

    if required_page == 'questions':
        to_count = Question.objects

    elif required_page == 'answers':
        to_count = Answer.objects

    elif 'tag' in required_page:
        to_count = get_tag(extra_context['tagname']).question_set

    elif required_page == 'question':
        try:
            to_count = extra_context['q'].answer_set
        except:
            raise Http404

    else:
        raise Http404

    tags = get_top_tags(30)
    new_users = get_users(10)
    pages_count = int(ceil(get_count(to_count) / 30 + 1))
    page_left, page_right = get_pages_bounds(pages_count, current_page)
    pages = range(page_left, page_right + 1)
    all_tags = get_all_tags()

    d = {'tags': tags,
         'new_users': new_users,
         'pages': pages,
         'pages_count': pages_count,
         'current_page': current_page,
         'all_tags': all_tags,
         'required_page': required_page,
         'form': form,
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
        elif tab == 'popular':
            c['res'] = get_questions_by_rating(current_page)
        else:
            raise Http404
    c['page'] = '/questions/' + tab
    c['tab'] = tab
    return get_response(request, 'questions', c, current_page)


def new_questions(request):
    return questions(request, 'new')


def popular_questions(request):
    return questions(request, 'popular')


def answers(request, tab):
    if not tab and tab is not None:
        tab = 'new'

    current_page = get_page(request)
    c = {}
    if tab is not None:
        if tab == 'new':
            c['res'] = get_answers_by_date(current_page)
        elif tab == 'popular':
            c['res'] = get_answers_by_rating(current_page)
        else:
            raise Http404
    c['page'] = '/answers/' + tab
    c['tab'] = tab
    return get_response(request, 'answers', c, current_page)


def new_answers(request):
    return answers(request, 'new')


def popular_answers(request):
    return answers(request, 'popular')


def users(request):
    return None


def question_page(request, q_id):
    q = get_question(q_id)
    answerform_error = False
    if request.method == 'POST' and 'form_type' in request.POST and request.POST['form_type'] == 'answer':
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login')
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            contents = answer_form.cleaned_data['contents']
            ans = Answer(question=q, author=request.user, date=datetime.datetime.today(), correct=False, rating=0, contents=contents)
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
             'page': '/question/' + str(q_id),
             'answer_form': answer_form,
             'answerform_error': answerform_error}
    except:
        raise Http404

    return get_response(request, 'question', c, current_page)


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
         'page': '/users/' + user.username + '/' + tab,
         'current_page': page,
         'required_page': 'user'}

    return render(request, "index.html", c)


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
    c['tagname'] = tagname
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

            if ok:
                content.rating += value
                content.save()

                response_data = {
                    'msg': "Your vote accepted.",
                    'rating': content.rating
                }
            else:
                response_data = {
                    'msg': "You cannot vote twice.",
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


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST, request.FILES)
        if reg_form.is_valid():
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
    })