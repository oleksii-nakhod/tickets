from command.interface.command import *
from service.auth import *

class LoginCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        result = AuthService().login(self.request)
        return result