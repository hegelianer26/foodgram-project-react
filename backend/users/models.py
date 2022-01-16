from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    USER = 'user'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (ADMIN, 'admin')
    )
    email = models.EmailField(
        max_length=254, unique=True, help_text='Адрес электронной почты')
    username = models.CharField(
        max_length=150, unique=True, help_text='Уникальный юзернейм')
    first_name = models.CharField(
        max_length=150, verbose_name='Имя', help_text='Имя')
    last_name = models.CharField(
        max_length=150, verbose_name='Фамилия', help_text='Фамилия')
    password = models.CharField(
        max_length=150, verbose_name='Пароль', help_text='Пароль')
    role = models.CharField(
        max_length=20, verbose_name='Роль', choices=ROLE_CHOICES,
        default=USER, help_text='Роль пользователя')

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Кто подписывается?')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='На кого подписывемся')

    def __str__(self):
        return (f'{self.user.username} на {self.author.username}')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(
            fields=['author', 'user'],
            name='unique_follows'
        )]
