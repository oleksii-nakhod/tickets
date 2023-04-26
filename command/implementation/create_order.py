from command.interface.command import *
from service.order import *

class CreateOrderCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        result = OrderService().create(self.request)
        return result