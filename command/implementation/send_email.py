from command.interface.command import *
from service.mail import *

class SendEmailCommand(ICommand):
    def __init__(self, to_email, template_id, dynamic_template_data):
        self.to_email = to_email
        self.template_id = template_id
        self.dynamic_template_data = dynamic_template_data
        
    def execute(self):
        result = MailService().send(self.to_email, self.template_id, self.dynamic_template_data)
        return result