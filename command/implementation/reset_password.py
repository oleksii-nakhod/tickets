from command.interface.command import *
from service.auth import *

class ResetPasswordCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        password = self.request.json['password']
        result = AuthService().reset_password(password)
        return result