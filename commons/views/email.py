from django.shortcuts import render
from django.http import HttpResponse

from commons.tasks.email import send_email


def enviar_email(request):
    if request.method == 'POST':
        # Recupere os destinatários do formulário (pode ser uma lista de e-mails)
        recipient_list = request.POST.getlist('recipient_list')

        # Recupere o assunto e a mensagem do formulário
        subject = request.POST['subject']
        message = request.POST['message']

        # Crie um dicionário com o assunto e a mensagem
        email_preset = {'subject': subject, 'message': message}

        # Chame a função send_email para enviar o e-mail
        send_email(recipient_list, email_preset)

        return HttpResponse('E-mail enviado com sucesso!')

    return render(request, 'test_email.html')  # Crie um template HTML para o formulário de envio de e-mail
