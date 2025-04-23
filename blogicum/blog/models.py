from django.contrib.auth import get_user_model
from django.db.models import (
    BooleanField,
    CharField,
    CASCADE,
    DateTimeField,
    ForeignKey,
    ImageField,
    Model,
    SlugField,
    SET_NULL,
    TextField,
)

from .decorators import cut_str

MAX_LENGTH_CHARS = 256


class CreatedModel(Model):
    created_at = DateTimeField(auto_now_add=True,
                               verbose_name='Added')

    class Meta:
        abstract = True


class PublishedCreatedModel(CreatedModel):
    is_published = BooleanField(default=True,
                                verbose_name='Published',
                                help_text='Uncheck the box to '
                                'hide the post.')

    class Meta:
        abstract = True


class Location(PublishedCreatedModel):
    name = CharField(max_length=MAX_LENGTH_CHARS,
                     verbose_name='Place name')

    class Meta:
        verbose_name = 'locations'
        verbose_name_plural = 'Locations'

    @cut_str
    def __str__(self):
        return self.name


class Category(PublishedCreatedModel):
    title = CharField(max_length=MAX_LENGTH_CHARS,
                      verbose_name='Heading')
    description = TextField(verbose_name='Description')
    slug = SlugField(unique=True,
                     verbose_name='Identifier',
                     help_text=('Page ID for URL; Latin characters, numbers,'
                                'hyphens and underscores are allowed.'))

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Category'

    @cut_str
    def __str__(self):
        return self.title


class Post(PublishedCreatedModel):
    title = CharField(max_length=MAX_LENGTH_CHARS,
                      verbose_name='Heading')
    text = TextField(verbose_name='Text')
    image = ImageField(
        verbose_name='Photo',
        upload_to='posts_images',
        blank=True
    )
    pub_date = DateTimeField(
        verbose_name='Date and time of publication',
        help_text=(
            'If you set the date and time in the future,'
            ' you can make scheduled publications.'
        )
    )
    author = ForeignKey(
        get_user_model(),
        related_name='posts',
        on_delete=CASCADE,
        verbose_name='Author of the publication'
    )
    location = ForeignKey(
        Location,
        related_name='posts',
        on_delete=SET_NULL,
        null=True,
        verbose_name='Location'
    )
    category = ForeignKey(
        Category,
        related_name='posts',
        on_delete=SET_NULL,
        null=True,
        verbose_name='Category'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Publication'
        verbose_name_plural = 'Publication'

    @cut_str
    def __str__(self):
        return self.title


class Comment(CreatedModel):
    text = TextField(verbose_name='Text')
    author = ForeignKey(get_user_model(),
                        related_name='comments',
                        on_delete=CASCADE,
                        verbose_name='Author')
    post = ForeignKey(Post,
                      related_name='comments',
                      on_delete=CASCADE,
                      verbose_name='Post')

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'comment'

    @cut_str
    def __str__(self):
        return self.text
