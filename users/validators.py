import re
from django.core.exceptions import ValidationError
from django.conf import settings
from django.templatetags.i18n import language


def validate_password(field):
    pattern = re.compile(r'^[A-Za-z0-9]+$')
    language = settings.LANGUAGE_CODE
    error_messages = [
        {
            'en-us': "Must contain A-Z, a-z letters and 0-9 numbers",
            'ru-ru': "Должен содержать буквы A-Z, a-z и цифры 0-9"
        },
        {
            'en-us': "Password length must be between 8 and 16 characters",
            'ru-ru': "Длина пароля должна быть от 8 до 16 символов"
        }
    ]
    if not bool(re.match(pattern, field)):
        raise ValidationError(error_messages[0][language], code=error_messages[0][language])
    if not 8 <= len(field) <= 16:
        raise ValidationError(error_messages[1][language], code=error_messages[1][language])
