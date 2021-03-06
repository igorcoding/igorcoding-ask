# coding=utf8
import sys, os
sys.path.append('/home/igor/Documents/www/igorcoding_ask/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'igorcoding_ask.settings'

import string
import random
import datetime
from django.contrib.auth.models import User
from random_words import *
import time
import MySQLdb


def value_in_dict_arr(dict_arr, key, value):
    for dictionary in dict_arr:
        if key in dictionary and dictionary[key] == value:
            return True
    return False


def get_random_number(number_length_max=7, extra=""):
    return ''.join(random.choice(string.digits + extra) for x in range(random.randint(1, number_length_max)))


def get_random_datetime():
    return datetime.datetime(random.randint(1900, 2012),
                             random.randint(1, 12),
                             random.randint(1, 28),
                             random.randint(0, 23),
                             random.randint(0, 59),
                             random.randint(0, 59),
                             random.randint(0, 1000))


def generate_users(connection, cursor, usersCount):
    print "Generating %d users..." % usersCount

    users = []
    finalusers = []
    while len(users) < usersCount:
        user = {
            "username": None,
            "first_name": None,
            "last_name": None,
            "password": None,
            "email": None,
            "date_joined": None,
            "last_login": None
        }
        randusername = RandomNicknames().random_nick(None, 'u')

        if not value_in_dict_arr(users, "username", randusername):
            user["username"] = randusername
        else:
            temp = randusername
            while value_in_dict_arr(users, "username", temp):
                temp = randusername + get_random_number()
            user["username"] = temp

        user["first_name"] = RandomNicknames().random_nick(None, 'u')
        user["last_name"] = RandomNicknames().random_nick(None, 'u')
        user["password"] = RandomWords().random_word() + \
                           get_random_number(2, "_.$#<>{}[]*^!+=-") + \
                           RandomWords().random_word()
        user["email"] = RandomEmails().randomMail()
        user["date_joined"] = get_random_datetime()
        last_login_date = get_random_datetime()
        while last_login_date < user["date_joined"]:
            last_login_date = get_random_datetime()
        user["last_login"] = last_login_date

        users.append(user)
        cursor.execute('INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                       (user["password"], user["last_login"], 0, user["username"],
                        user["first_name"], user["last_name"], user["email"], 0, 1, user["date_joined"],))
        connection.commit()

        finalusers.append(user["date_joined"])

        user_rating = random.randint(-50, 100)
        cursor.execute('INSERT INTO ask_userprofile (user_id, rating) VALUES (%s, %s)', (len(users)+1, user_rating))
        connection.commit()

        obj = User.objects.get(pk=(len(users)+1))
        obj.set_password(user["password"])
        obj.save()


    print "Users generated."
    return finalusers


def generate_tags(connection, cursor, tagsCount):
    print "Generating %s tags..." % tagsCount

    tags = []
    while len(tags) < tagsCount:
        tag = {
            "tagname": None
        }
        randTag = RandomWords().random_word()
        while value_in_dict_arr(tags, "tagname", randTag):
            randTag = RandomWords().random_word()
        tag["tagname"] = randTag

        tags.append(tag)
        cursor.execute('INSERT INTO ask_tag (tagname) VALUES (%s);',
                       (tag["tagname"],))
        connection.commit()

    print "Tags generated."
    return tags


def generate_questions(connection, cursor, questionsCount, users, tags):
    print "Generating %s questions..." % questionsCount

    TAGS_PER_QUESTION = 3
    questions = []
    while len(questions) < questionsCount:
        question = {
            "title": None,
            "contents": None,
            "author_id": None,
            "creation_date": None,
            "tags": [],
            "rating": None
        }

        lorem = LoremIpsum()
        lorem.MAX_WORDS = 20

        question["title"] = lorem.get_sentence()
        question["contents"] = lorem.get_sentences(random.randint(2, 12))
        question["author_id"] = random.randint(2, len(users)+1)
        creation_date = get_random_datetime()
        while creation_date < users[question["author_id"] - 2]:
            creation_date = get_random_datetime()
        question["creation_date"] = creation_date
        q_tags = []
        while len(q_tags) < TAGS_PER_QUESTION:
            tag = random.randint(0, len(tags) - 1)
            if tag not in q_tags:
                q_tags.append(tag)
        question["tags"] = q_tags

        voted_users = set([])
        plus_one = random.randint(0, 99)
        minus_one = random.randint(0, 20)

        #question["rating"] = plus_one - minus_one
        question["rating"] = random.randint(-900, 900)

        cursor.execute('INSERT INTO ask_question (title, contents, author_id, creation_date, rating) VALUES (%s, %s, %s, %s, %s);',
                      (question["title"], question["contents"], question["author_id"], question["creation_date"], question["rating"]))
        connection.commit()
        """
        for x in range(0, plus_one):
            rand_user = random.randint(2, len(users)+1)
            while rand_user in voted_users:
                rand_user = random.randint(2, len(users)+1)
            voted_users.add(rand_user)
            cursor.execute('INSERT INTO ask_questionvote (user_id, question_id, value) values (%s, %s, %s);',
                           (rand_user, len(questions)+1, 1))
            connection.commit()

        for x in range(0, minus_one):
            rand_user = random.randint(2, len(users)+1)
            while rand_user in voted_users:
                rand_user = random.randint(2, len(users)+1)
            cursor.execute('INSERT INTO ask_questionvote (user_id, question_id, value) values (%s, %s, %s);',
                           (rand_user, len(questions)+1, -1))
            connection.commit()
            """

        questions.append(question["creation_date"])

        for i in range(len(question["tags"])):
            cursor.execute('INSERT INTO ask_question_tag (question_id, tag_id) VALUES (%s, %s);',
                          (len(questions), question["tags"][i] + 1))
            connection.commit()

    print "Questions generated."
    return questions


def generate_answers(connection, cursor, answersCount, questions, users):
    print "Generating %s answers..." % answersCount

    #answers = []
    n = 0
    while n < answersCount:
        if n % 1000 == 0:
            print "%d answers generated....." % n
        answer = {
            "contents": None,
            "question_id": None,
            "author_id": None,
            "date": None,
            "correct": None,
            "rating": None
        }

        lorem = LoremIpsum()
        lorem.MAX_WORDS = 20

        answer["contents"] = lorem.get_sentences(random.randint(2, 12))
        answer["question_id"] = random.randint(1, len(questions))
        answer["author_id"] = random.randint(2, len(users) + 1)
        answer_date = get_random_datetime()
        while answer_date < questions[answer["question_id"] - 1]:
            answer_date = get_random_datetime()
        answer["date"] = answer_date
        answer["correct"] = random.randint(0, 1)

        voted_users = set([])
        plus_one = random.randint(0, 99)
        minus_one = random.randint(0, 20)

        #answer["rating"] = plus_one - minus_one
        answer["rating"] = random.randint(-900, 900)

        #answers.append(answerif (len(answers) ))

        cursor.execute('INSERT INTO ask_answer (contents, question_id, author_id, correct, rating, date) VALUES (%s, %s, %s, %s, %s, %s);',
                      (answer["contents"], answer["question_id"], answer["author_id"], answer["correct"], answer["rating"], answer["date"]))
        connection.commit()
        """
        for x in range(0, plus_one):
            rand_user = random.randint(2, len(users)+1)
            while rand_user in voted_users:
                rand_user = random.randint(2, len(users)+1)
            voted_users.add(rand_user)
            cursor.execute('INSERT INTO ask_answervote (user_id, answer_id, value) values (%s, %s, %s);',
                           (rand_user, n+1, 1))
            connection.commit()

        for x in range(0, minus_one):
            rand_user = random.randint(2, len(users)+1)
            while rand_user in voted_users:
                rand_user = random.randint(2, len(users)+1)
            cursor.execute('INSERT INTO ask_answervote (user_id, answer_id, value) values (%s, %s, %s);',
                           (rand_user, n+1, -1))
            connection.commit()
        """

        n += 1

    print "Answers generated."
    #return answers


MAX_USERS = 10000
MAX_TAGS = 100
MAX_QUESTIONS = 100000
MAX_ANSWERS = 1000000


def main():
    connection = MySQLdb.connect('localhost', 'ask_db_user', 'user_pass', 'ask_db')

    cursor = connection.cursor()

    now = time.time()
    users_res = generate_users(connection,  cursor, MAX_USERS)
    print "Time: %d" % (time.time() - now)

    '''now = time.time()
    tags_res = generate_tags(connection, cursor, MAX_TAGS)
    print "Time: %d" % (time.time() - now)

    now = time.time()
    questions_res = generate_questions(connection, cursor, MAX_QUESTIONS, users_res, tags_res)
    print "Time: %d" % (time.time() - now)

    now = time.time()
    generate_answers(connection, cursor, MAX_ANSWERS, questions_res, users_res)

    print "Time: %d" % (time.time() - now)
'''
    connection.close()

if __name__ == "__main__":
    main()



