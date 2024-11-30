from django.db import models
from django.conf import settings
from users.models import NULLABLE


class Category(models.Model):
    """
    Представляет категорию породы для собак.

    Атрибуты:
        name (str): Название породы.
        description (str): Описание породы.
    """

    name = models.CharField(max_length=100, verbose_name="breed")
    description = models.CharField(max_length=1000, verbose_name="description")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'


class Dog(models.Model):
    """
    Представляет собаку в системе.

    Атрибуты:
        name (str): Имя собаки.
        category (Category): Порода собаки.
        photo (ImageField): Фото собаки.
        birth_date (date): Дата рождения собаки.
    """

    name = models.CharField(max_length=250, verbose_name="dog_name")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="breed")
    photo = models.ImageField(upload_to='dogs/', verbose_name="photo", **NULLABLE)
    birth_date = models.DateField(verbose_name="birth_date", **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name="Владелец")

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'dog'
        verbose_name_plural = 'dogs'
