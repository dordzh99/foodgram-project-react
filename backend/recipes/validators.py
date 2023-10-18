from django.core.exceptions import ValidationError

from .models import Tag


def validate_unique_color(value):
    if Tag.objects.filter(color=value).exists():
        raise ValidationError('Тег с таким цветом уже существует.')
