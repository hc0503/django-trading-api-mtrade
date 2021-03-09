# import django
from django.core.mail import EmailMessage

class Mail(EmailMessage):
    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
                 connection=None, attachments=None, headers=None, cc=None,
                 reply_to=None, template_id=None, dynamic_template_data=None):
        super().__init__(subject, body, from_email, to, bcc, connection, attachments, headers, cc, reply_to)
        self.template_id = template_id
        self.dynamic_template_data = dynamic_template_data
