from django.contrib.auth import get_user_model
from django.forms import DateTimeInput
from django.forms.models import ModelForm

from .models import Post, Comment

User = get_user_model()


class PostModelForm(ModelForm):

    class Meta:
        model = Post
        exclude = ['author']
        widgets = {
            'pub_date': DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentModelForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text']