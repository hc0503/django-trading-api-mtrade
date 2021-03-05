# import django
from django.core.mail import EmailMessage

class Mail():
    def __init__(self, from_email, to, template_id, dynamic_template_data, **kwargs):
        self.from_email = from_email
        self.to = to
        self.template_id = template_id
        self.dynamic_template_data = dynamic_template_data

        self.__dict__.update(kwargs)
    
    def send(self):
        msg = EmailMessage(
            from_email = self.from_email,
            to = self.to,
        )
        
        msg.template_id = self.template_id
        msg.dynamic_template_data = self.dynamic_template_data
        
        if 'reply_to' in globals():
            msg.reply_to = self.reply_to

        if 'cc' in globals():
            msg.cc = self.cc
        
        if 'bcc' in globals():
            msg.bcc = self.bcc

        try:
            msg.send(fail_silently=False)
        except Exception as e:
            raise Exception(e)
        
        return True