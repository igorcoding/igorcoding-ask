from django.conf.urls import patterns, url

from ask import views
from igorcoding_ask import settings

urlpatterns = patterns('',
    url(r'^$', views.new_questions, name='index'),
    url(r'new', views.new_questions, name='new'),
    url(r'popular', views.popular_questions, name='popular')
)