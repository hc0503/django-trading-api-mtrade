# import django
from django.core.mail import EmailMessage

class Mail(EmailMessage):
    def send(self):
        result = super(Mail, self).send()

        return result