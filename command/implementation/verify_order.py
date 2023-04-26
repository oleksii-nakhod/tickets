from command.interface.command import *
from service.order import *

class VerifyOrderCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        result = OrderService().verify(self.request)
        return result