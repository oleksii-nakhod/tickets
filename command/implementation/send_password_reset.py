from command.interface.command import *
from service.auth import *

class SendPasswordResetCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        email = self.request.json['email']
        result = AuthService().send_password_reset(email)
        return result