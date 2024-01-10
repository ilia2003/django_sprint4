from django.urls import path, include

from . import views


app_name = 'blog'


profile_urls = [
    path('<str:username>/',
         views.ProfileDetailView.as_view(), name='profile'),
    path('current/edit/',
         views.ProfileUpdateView.as_view(), name='edit_profile'),
]

posts_urls = [
    path('create/',
         views.PostCreateView.as_view(), name='create_post'),
    path('<int:post_id>/delete/',
         views.PostDeleteView.as_view(), name='delete_post'),
    path('<int:post_id>/edit/',
         views.PostUpdateView.as_view(), name='edit_post'),
    path('<int:post_id>/',
         views.PostDetailView.as_view(), name='post_detail'),

    path('<slug:post_id>/comment/',
         views.CommentCreateView.as_view(), name='add_comment'),
    path('<slug:post_id>/edit_comment/<int:comment_id>/',
         views.CommentUpdateView.as_view(), name='edit_comment'),
    path('<slug:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(), name='delete_comment'),
]

category_urls = [
    path('<slug:category_slug>/',
         views.CategoryDetailView.as_view(), name='category_posts'),
]

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('profile/', include(profile_urls)),
    path('posts/', include(posts_urls)),
    path('category/', include(category_urls)),
]