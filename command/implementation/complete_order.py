from command.interface.command import *
from service.order import *

class CompleteOrderCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        result = OrderService().complete(self.request)
        return result