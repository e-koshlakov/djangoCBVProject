from django.conf import settings
from django.core.mail import send_mail

def send_registration_email(email):
    send_mail(
    subject = 'Активация аккаунта',
    message = f'Вы успешно зарегистрировались на сайте.',
    from_email = settings.EMAIL_HOST_USER,
    recipient_list = [email]
    )
