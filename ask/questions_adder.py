import random
import sys, os
import math
from threading import Timer
from random_words import RandomWords
import time
from ask.generate_data import value_in_dict_arr, get_random_number
from ask.models import Tag

sys.path.append('/home/igor/Documents/www/igorcoding_ask/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'igorcoding_ask.settings'

from django.test import Client


GENERATION_DELAY = 4  # seconds


def generate_rand_tag():
    tags = Tag.objects.all()
    rand_tag = RandomWords().random_word()
    while Tag(tagname=rand_tag) in tags:
        rand_tag = RandomWords().random_word() + get_random_number()
    return rand_tag


def postpone_func(function, time, *args):
    t = Timer(time, function, args)
    t.start()


def generate_question(client, title, contents, tags):
    data = {'title': title,
            'contents': contents,
            'tags': tags,
            'form_type': 'ask'}
    post = client.post("http://localhost/questions/new", data)

    print post.status_code


def main():
    client = Client()
    logged_in = client.login(username="generator", password="generator")
    print "Logged in: %s" % logged_in
    #login = client.post('http://localhost/login/', {"username": "generator", "password": "generator"}, follow=True)

    num = 0
    while True:
        tags = Tag.objects.all()
        max_tags = len(tags)
        tag_id = random.randint(0, max_tags)
        if tag_id == max_tags:
            tag = generate_rand_tag()
        else:
            tag = tags[tag_id]

        generate_question(client, str(num), str(num), tag)
        time.sleep(GENERATION_DELAY)
        num += 1


if __name__ == "__main__":
    main()