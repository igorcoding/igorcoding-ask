from django.forms import *
from ask.models import *


class TagsField(CharField):
    def to_python(self, value):
        return value.split(',')

    def validate(self, value):
        super(TagsField, self).validate(value)
        for tag in value:
            print tag


class AskForm(forms.Form):
    title = CharField(max_length=255, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Question title'
    }))
    contents = CharField(widget=Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your question right here',
        'rows': '11'
    }))
    tags = TagsField(required=False, widget=HiddenInput())


class AnswerForm(forms.Form):
    contents = CharField(widget=Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your answer right here',
        'rows': '11',
        'style': 'resize:vertical;'
    }))