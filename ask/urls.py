from django.conf.urls import patterns, url

from ask import views
from igorcoding_ask import settings

urlpatterns = patterns('',
    url(r'^$', views.new_questions, name='index'),
    url(r'popular', views.popular_questions, name='popular'),
    url(r'question', views.question_page, name='question'),
    url(r'qrating', views.change_question_rating),
    url(r'answers', views.new_answers),
    url(r'answers/popular', views.popular_answers),
    url(r'users', views.users)
)