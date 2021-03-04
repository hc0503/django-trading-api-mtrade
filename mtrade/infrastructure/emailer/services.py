# import django
from django.core.mail import EmailMessage

class EmailerServices():
    def send(self, templateId, templateData, fromEmail, toEmail, replyTo=None):
        msg = EmailMessage(
            from_email = fromEmail,
            to = toEmail
        )
        msg.template_id = templateId
        msg.template_data = templateData
        msg.reply_to = replyTo

        try:
            msg.send(fail_silently=False)
        except Exception as e:
            raise Exception(e)
        
        return True