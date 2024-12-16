from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from dogs.models import Category
from dogs.models import Dog

def get_categories_cache():
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        if not category_list:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()

    return category_list


def send_email(dog_object, owner_email, views_count):
    subject = f'Ваша собака "{dog_object}" была просмотрена {views_count} раз'
    message = f'Поздравляем! Ваша собака "{dog_object}" была просмотрена {views_count} раз'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [owner_email,]
    send_mail(subject, message, email_from, recipient_list)