from command.interface.command import *
from service.auth import *

class SignupCommand(ICommand):
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        
    def execute(self):
        result = AuthService().signup(self.name, self.email, self.password)
        return result