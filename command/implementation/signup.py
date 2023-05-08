from command.interface.command import *
from service.auth import *

class SignupCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        name = self.request.json['name']
        email = self.request.json['email']
        password = self.request.json['password']
        result = AuthService().signup(name, email, password)
        return result