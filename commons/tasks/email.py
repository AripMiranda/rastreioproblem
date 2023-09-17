from django.core.mail import send_mail
from django.http import HttpResponse

from tracking.settings import EMAIL_HOST_USER


def send_email(recipient_list: list, email_preset: dict = {}):
    subject = email_preset.get('subject', 'Assunto do E-mail')
    message = email_preset.get('message', 'Conteúdo do E-mail')
    from_email = EMAIL_HOST_USER

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return HttpResponse('E-mail enviado com sucesso!')
