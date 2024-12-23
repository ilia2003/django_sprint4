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
                               verbose_name='Добавлено')

    class Meta:
        abstract = True


class PublishedCreatedModel(CreatedModel):
    is_published = BooleanField(default=True,
                                verbose_name='Опубликовано',
                                help_text='Снимите галочку, '
                                          'чтобы скрыть публикацию.')

    class Meta:
        abstract = True


class Location(PublishedCreatedModel):
    name = CharField(max_length=MAX_LENGTH_CHARS,
                     verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    @cut_str
    def __str__(self):
        return self.name


class Category(PublishedCreatedModel):
    title = CharField(max_length=MAX_LENGTH_CHARS,
                      verbose_name='Заголовок')
    description = TextField(verbose_name='Описание')
    slug = SlugField(unique=True,
                     verbose_name='Идентификатор',
                     help_text=(
                         'Идентификатор страницы для URL; '
                         'разрешены символы латиницы, цифры, дефис '
                         'и подчёркивание.'
                     ))

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    @cut_str
    def __str__(self):
        return self.title


class Post(PublishedCreatedModel):
    title = CharField(max_length=MAX_LENGTH_CHARS,
                      verbose_name='Заголовок')
    text = TextField(verbose_name='Текст')
    image = ImageField(
        verbose_name='Фото',
        upload_to='posts_images',
        blank=True
    )
    pub_date = DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить '
            'дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = ForeignKey(
        get_user_model(),
        related_name='posts',
        on_delete=CASCADE,
        verbose_name='Автор публикации'
    )
    location = ForeignKey(
        Location,
        related_name='posts',
        on_delete=SET_NULL,
        null=True,
        verbose_name='Местоположение'
    )
    category = ForeignKey(
        Category,
        related_name='posts',
        on_delete=SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    @cut_str
    def __str__(self):
        return self.title


class Comment(CreatedModel):
    text = TextField(verbose_name='Текст')
    author = ForeignKey(get_user_model(),
                        related_name='comments',
                        on_delete=CASCADE,
                        verbose_name='Автор')
    post = ForeignKey(Post,
                      related_name='comments',
                      on_delete=CASCADE,
                      verbose_name='Публикация')

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    @cut_str
    def __str__(self):
        return self.text
