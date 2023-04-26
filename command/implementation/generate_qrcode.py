from command.interface.command import *
from service.order import *

class GenerateQrcodeCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        result = OrderService().generate_qrcode(self.request)
        return result