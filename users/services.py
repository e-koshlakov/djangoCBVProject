from django.conf import settings
from django.core.mail import send_mail

def send_registration_email(email):
    send_mail(
    subject = 'Активация аккаунта',
    message = f'Вы успешно зарегистрировались на сайте.',
    from_email = settings.EMAIL_HOST_USER,
    recipient_list = [email]
    )

def send_new_password_email(email, new_password):
    send_mail(
    subject = 'Новый пароль',
    message = f'Ваш новый пароль: {new_password}',
    from_email = settings.EMAIL_HOST_USER,
    recipient_list = [email]
    )
