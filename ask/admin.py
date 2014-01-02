from django.contrib import admin
from ask.models import *


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'contents', 'author', 'creation_date', 'rating')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('contents', 'question', 'author', 'date', 'correct', 'rating')


class QuestionVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'value')


class AnswerVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer', 'value')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionVote, QuestionVoteAdmin)
admin.site.register(Answer)
admin.site.register(AnswerVote, AnswerVoteAdmin)
admin.site.register(Tag)
admin.site.register(UserProfile, UserProfileAdmin)