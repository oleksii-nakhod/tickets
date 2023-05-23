from command.interface.command import *
from service.auth import *

class ConfirmAccountCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        id = self.request.args.get('id')
        token = self.request.args.get('token')
        result = AuthService().confirm(id, token)
        return result