from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('user', 'Regular User'),
    )

    # Переопределяем поле groups с уникальным related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='группы',
        help_text='Группы, к которым принадлежит пользователь',
    )

    # Переопределяем поле user_permissions с уникальным related_name
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='права пользователя',
        help_text='Специфические права для этого пользователя',
    )

    role = models.CharField(max_length=20, choices=ROLES, default='user')
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def is_admin_user(self):
        return self.role == 'admin'

    def is_manager(self):
        return self.role == 'manager'
