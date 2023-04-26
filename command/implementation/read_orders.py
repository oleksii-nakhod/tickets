from command.interface.command import *
from service.order import *

class ReadOrdersCommand(ICommand):
    def __init__(self):
        pass
        
    def execute(self):
        result = OrderService().read()
        return result