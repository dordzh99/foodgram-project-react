from django.contrib.auth.models import AbstractUser
from django.db import models

from .constant import LENGTH_EMAIL


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    is_subscribed = models.BooleanField(default=False)


class Subscribe(models.Model):
    """Модель подписки на автора."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscriber',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='following',
    )

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user_is_not_following_himself',
            ),
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follow'),
        )
        ordering = ('-user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'{self.user.username} подписан на {self.author.username}'
