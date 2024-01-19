from django.db.models import QuerySet, Count
from django.utils import timezone

from .models import Post


def get_posts(to_filter: bool = False,
              count_comments: bool = False) -> QuerySet:
    posts = Post.objects.select_related('author', 'category', 'location')
    if to_filter:
        posts = (posts
                 .filter(is_published=True,
                         pub_date__lte=timezone.now(),
                         category__is_published=True))
    if count_comments:
        posts = (posts
                 .annotate(comment_count=Count('comments'))
                 .order_by("-pub_date"))
    return posts
