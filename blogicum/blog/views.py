from datetime import datetime as dt

from django.db.models import QuerySet
from django.views.generic import (
    DetailView,
    UpdateView,
    ListView,
    CreateView,
    DeleteView,
)
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count

from .models import Post, Category, Comment
from .forms import PostModelForm, CommentModelForm


User = get_user_model()


class GetPostDetailUrlMixin:

    def get_success_url(self):
        return reverse('blog:post_detail',
                       args=[self.kwargs['post_id']])


class CommentModificationPermissionMixin(LoginRequiredMixin,
                                         GetPostDetailUrlMixin):

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment,
                                    id=kwargs['comment_id'],
                                    post_id=kwargs['post_id'])
        if request.user != comment.author:
            return redirect(self.get_success_url(), permanent=True)
        return super().dispatch(request, *args, **kwargs)


class PostModificationPermissionMixin(LoginRequiredMixin,
                                      GetPostDetailUrlMixin):

    def dispatch(self, request, *args, **kwargs):
        author = self.get_object().author
        auth_user = request.user
        if auth_user != author:
            return redirect(self.get_success_url(),
                            permanent=True)
        return super().dispatch(request, *args, **kwargs)


def get_posts(to_filter: bool = False,
              count_comments: bool = False) -> QuerySet:
    posts = Post.objects.select_related('author', 'category', 'location')
    if to_filter:
        posts = (posts
                 .filter(is_published=True,
                         pub_date__lte=dt.now(),
                         category__is_published=True))
    if count_comments:
        posts = (posts
                 .annotate(comment_count=Count('comments'))
                 .order_by("-pub_date"))
    return posts


class ProfileDetailView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    paginate_by = 10

    def get_author(self) -> User:
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        auth_user = self.request.user
        author = self.get_author()
        return (get_posts(to_filter=(author != auth_user),
                          count_comments=True)
                .filter(author=author))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['profile'] = self.get_author()
        return ctx


class ProfileUpdateView(LoginRequiredMixin,
                        UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ['email', 'first_name', 'last_name', 'is_active', 'date_joined']

    def get_success_url(self):
        return reverse('blog:profile',
                       args=[self.get_object().username])

    def get_object(self, queryset=None):
        return self.request.user


class PostCreateView(LoginRequiredMixin,
                     CreateView):
    model = Post
    form_class = PostModelForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile',
                       args=[self.request.user.username])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(PostModificationPermissionMixin,
                     DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:index')


class PostUpdateView(PostModificationPermissionMixin,
                     UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    post_id_kwarg = 'post_id'


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10
    queryset = get_posts(to_filter=True,
                         count_comments=True)


class PostDetailView(DetailView):
    queryset = get_posts()
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post: Post = super().get_object(queryset)
        author = post.author
        auth_user = self.request.user
        if (author != auth_user
                and (not post.is_published
                     or not post.category.is_published
                     or post.pub_date > dt.now(tz=post.pub_date.tzinfo))):
            raise Http404('Пост не найден')
        return post

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = ctx['post']
        ctx['comments'] = (Comment.objects.select_related('author')
                           .filter(post=post))
        ctx['form'] = CommentModelForm()
        return ctx


class CategoryDetailView(ListView):
    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    paginate_by = 10

    def get_category(self):
        return get_object_or_404(Category,
                                 slug=self.kwargs[self.slug_url_kwarg],
                                 is_published=True)

    def get_queryset(self):
        category = self.get_category()
        return (get_posts(to_filter=True,
                          count_comments=True)
                .filter(category=category))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        category = self.get_category()
        ctx['category'] = category
        return ctx


class CommentCreateView(LoginRequiredMixin,
                        GetPostDetailUrlMixin,
                        CreateView):
    model = Comment
    form_class = CommentModelForm
    template_name = 'blog/comment.html'
    slug_field = 'post_id'
    slug_url_kwarg = 'post_id'

    def form_valid(self, form):
        post = get_object_or_404(Post,
                                 id=self.kwargs[self.slug_field])
        auth_user = self.request.user
        form.instance.post = post
        form.instance.author = auth_user
        return super().form_valid(form)


class CommentUpdateView(CommentModificationPermissionMixin,
                        UpdateView):
    model = Comment
    form = CommentModelForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    slug_url_kwarg = 'post_id'
    fields = ['text']


class CommentDeleteView(CommentModificationPermissionMixin,
                        DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    slug_url_kwarg = 'post_id'
    template_name = 'blog/comment.html'
    context_object_name = 'comment'
