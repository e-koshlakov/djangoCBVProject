from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    last_name = models.CharField(max_length=50, default='Anonymous')
    first_name = models.CharField(max_length=50, default='Anonymous')
    # pk = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, **NULLABLE)
    address = models.TextField(**NULLABLE)
    date_of_birth = models.DateField(**NULLABLE)
    telegram = models.CharField(max_length=50, verbose_name='Telegram Username', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Avatar', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='active')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']
