from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    username = models.CharField(verbose_name='Никнейм', max_length=64)
    first_name = models.CharField(verbose_name='Имя', max_length=64)
    last_name = models.CharField(verbose_name='Фамилия', max_length=64)
    password = models.CharField(verbose_name='Пароль', max_length=64)
    avatar = models.ImageField(blank=True, null=True, upload_to='media/avatar')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
