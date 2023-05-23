from command.interface.command import *
from service.order import *

class CreateQrcodeCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        ticket_id = self.request.args.get('ticket-id')
        result = OrderService().create_qrcode(ticket_id)
        return result