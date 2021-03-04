# import django
from django.core.mail import EmailMessage

class EmailerServices():
    def __init__(self, templateId, templateData, fromEmail, replyTo=None):
        self.templateId = templateId
        self.templateData = templateData
        self.replyTo = replyTo
        self.fromEmail = fromEmail

    def sendTo(self, toEmails=[]):
        msg = EmailMessage(
            from_email = self.fromEmail,
            to = toEmails,
        )
        msg.template_id = self.templateId
        msg.template_data = self.templateData
        msg.reply_to = self.replyTo

        try:
            msg.send(fail_silently=False)
        except Exception as e:
            raise Exception(e)
        
        return True
    
    def sendCC(self, toEmails=[], ccEmails=[]):
        msg = EmailMessage(
            from_email = self.fromEmail,
            to = toEmails,
            cc = ccEmails
        )
        msg.template_id = self.templateId
        msg.template_data = self.templateData
        msg.reply_to = self.replyTo

        try:
            msg.send(fail_silently=False)
        except Exception as e:
            raise Exception(e)
        
        return True
    
    def sendBCC(self, toEmails=[], bccEmails=[]):
        msg = EmailMessage(
            from_email = self.fromEmail,
            to = toEmails,
            bcc = bccEmails
        )
        msg.template_id = self.templateId
        msg.template_data = self.templateData
        msg.reply_to = self.replyTo

        try:
            msg.send(fail_silently=False)
        except Exception as e:
            raise Exception(e)
        
        return True