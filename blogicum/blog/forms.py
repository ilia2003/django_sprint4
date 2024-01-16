from .models import Post, Comment

from django.contrib.auth import get_user_model
from django.forms.models import ModelForm
from django.forms import DateTimeInput


User = get_user_model()


class PostModelForm(ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                      attrs={'class': 'datetimefield'}),
        }


class CommentModelForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
