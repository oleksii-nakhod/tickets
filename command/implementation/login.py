from command.interface.command import *
from service.auth import *

class LoginCommand(ICommand):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
    def execute(self):
        result = AuthService().login(self.email, self.password)
        return result