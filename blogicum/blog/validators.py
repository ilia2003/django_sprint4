from django.core.exceptions import ValidationError
from django.utils import timezone

NOW = timezone.now()


def real_time(value):
    if value.date() < timezone.NOW().date():
        raise ValidationError('Нельзя публиковать записи в прошлом')
