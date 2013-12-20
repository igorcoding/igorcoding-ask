from django.contrib.auth.forms import UserCreationForm
from django.forms import *
from ask.models import *


class TagsField(CharField):
    def to_python(self, value):
        return value.split(',')


class AskForm(forms.Form):
    title = CharField(max_length=255, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Question title',
        'autocomplete': 'off'
    }))
    contents = CharField(widget=Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your question right here',
        'rows': '11',
        'autocomplete': 'off'
    }))
    tags = TagsField(required=False, widget=HiddenInput())


class AnswerForm(forms.Form):
    contents = CharField(widget=Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your answer right here',
        'rows': '11',
        'style': 'resize:vertical;'
    }))


class RegistrationForm(UserCreationForm):
    first_name = CharField(max_length=30,
                           label="First name",
                           required=False)
    last_name = CharField(max_length=30,
                          label="Last name",
                          required=False)
    email = EmailField(label="Email")
    user_pic = FileField(label="Your userpic",
                         required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user