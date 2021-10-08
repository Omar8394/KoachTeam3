import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


# settings.configure()
def create_mail(user_mail, subject, template_name, context):
    template = get_template(template_name)
    content = template.render(context)
    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[
            user_mail
        ],
        cc=[]
    )
    message.attach_alternative(content, 'text/html')
    return message


def send_mail(message):
    try:
        thread = threading.Thread(target=message.send(fail_silently=False))
        thread.start()
        print("enviando correo")
    except:
        print("se ha producido un error al enviar el correo")
