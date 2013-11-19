from django.conf.urls import patterns, url

from ask import views
from igorcoding_ask import settings

urlpatterns = patterns('',
    url(r'^$', views.new_questions, name='index'),
    url(r'^popular', views.popular_questions),
    url(r'^answers/popular', views.popular_answers),
    url(r'^answers', views.new_answers),
    url(r'^users', views.users),
    url(r'^question', views.question_page),
    url(r'^user', views.user),

    url(r'^qrating', views.change_question_rating),
    url(r'^arating', views.change_answer_rating),
    url(r'^setcorrect', views.set_correct)

)