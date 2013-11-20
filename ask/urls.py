from django.conf.urls import patterns, url

from ask import views
from igorcoding_ask import settings

urlpatterns = patterns('',
    url(r'^$', views.new_questions, name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),

    url(r'^users/(?P<username>\S*)/(?P<tab>[A-Za-z]*)', views.user1),
    url(r'^users/(?P<username>\S*)', views.user1),

    url(r'^new', views.new_questions),
    url(r'^popular', views.popular_questions),


    url(r'^rating/(?P<content_type>\S+)/(?P<way>\S+)', views.change_content_rating),
    url(r'^setcorrect', views.set_correct),

    url(r'^user', views.user),

    url(r'^(?P<required_page>[A-Za-z]*)/(?P<tab>[A-Za-z]*)', views.get_response),




    #url(r'^users', views.users),
    #url(r'^question', views.question_page),
    #



)