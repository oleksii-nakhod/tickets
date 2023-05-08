from command.interface.command import *
from service.auth import *

class LoginCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        email = self.request.json['email']
        password = self.request.json['password']
        result = AuthService().login(email, password)
        return result