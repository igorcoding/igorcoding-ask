from django import template
from ask.basicscripts import *

register = template.Library()


@register.inclusion_tag('tags-cloud.html')
def top_tags():
    tags = get_top_tags(30)
    return {'tags': tags}


@register.inclusion_tag('new_users.html')
def new_users():
    users = get_users(10)
    return {'new_users': users}

