from command.interface.command import *
from service.order import *

class VerifyOrderCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        id = self.request.args.get('id')
        token = self.request.args.get('token')
        result = OrderService().verify(id, token)
        return result