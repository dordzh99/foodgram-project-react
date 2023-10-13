from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .constant import LENGTH_EMAIL, LENGTH_USER


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=LENGTH_USER,
        unique=True,
        blank=False,
        validators=[RegexValidator(r'^[\w.@+-]+\Z')],
    )
    email = models.EmailField(
        verbose_name='Почта',
        unique=True,
        max_length=LENGTH_EMAIL,
        blank=False
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=LENGTH_USER,
        blank=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=LENGTH_USER,
        blank=False
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=LENGTH_USER,
        blank=False,
        validators=[RegexValidator(r'^[\w.@+-]+\Z')],
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """Модель подписки на автора."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        related_name="subscriber",
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Автор рецепта",
        related_name="following",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F("author")),
                name="user_is_not_following_himself",
            ),
            models.UniqueConstraint(fields=["user", "author"],
                                    name="unique_follow"),
        ]
        ordering = ["-user"]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self) -> str:
        return f'{self.user.username} подписан на {self.author.username}'
