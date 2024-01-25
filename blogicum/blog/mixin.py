from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .forms import CommentModelForm, PostModelForm
from .models import Comment, Post


class GetPostDetailUrlMixin():

    def get_success_url(self):
        return reverse('blog:post_detail',
                       args=[self.kwargs['post_id']])


class CommentModificationPermissionMixin(GetPostDetailUrlMixin):
    model = Comment
    form_class = CommentModelForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    slug_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment,
                                    id=kwargs['comment_id'],
                                    post_id=kwargs['post_id'])
        if request.user != comment.author:
            return redirect(self.get_success_url(), permanent=True)
        return super().dispatch(request, *args, **kwargs)


class PostModificationPermissionMixin(GetPostDetailUrlMixin):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
    form_class = PostModelForm

    def dispatch(self, request, *args, **kwargs):
        author = self.get_object().author
        auth_user = request.user
        if auth_user != author:
            return redirect(self.get_success_url(),
                            permanent=True)
        return super().dispatch(request, *args, **kwargs)
