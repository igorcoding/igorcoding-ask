from django.conf.urls import patterns, url

from ask import views
from igorcoding_ask import settings

urlpatterns = patterns('',
    url(r'^$', views.new_questions, name='index'),
    url(r'^login/$', views.my_login),
    url(r'^logout/$', views.my_logout),
    url(r'^signup/$', views.register),

    url(r'^users/$', views.users),
    url(r'^users/(?P<username>\S*)/(?P<tab>[A-Za-z]*)', views.user1),
    url(r'^users/(?P<username>\S*)', views.user1),


    url(r'^question/(?P<q_id>\d+)', views.question_page),
    url(r'^questions/(?P<tab>\S*)', views.questions),
    url(r'^answers/(?P<tab>\S*)', views.answers),
    url(r'^new', views.new_questions),
    url(r'^popular', views.popular_questions),

    url(r'^tag/(?P<tagname>\S+)/(?P<tab>\S*)', views.tag_search),
    url(r'^search/(?P<tab>\S*)', views.search),


    url(r'^rating/(?P<content_type>\S+)/(?P<way>\S+)', views.change_content_rating),
    url(r'^setcorrect', views.set_correct),

    #url(r'^(?P<required_page>[A-Za-z]*)/(?P<tab>[A-Za-z]*)', views.get_response),

)