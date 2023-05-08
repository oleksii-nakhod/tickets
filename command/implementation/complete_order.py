from command.interface.command import *
from service.order import *

class CompleteOrderCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        payload = self.request.get_data(as_text=True)
        sig_header = self.request.headers.get('Stripe-Signature')
        checkout_session_id = self.request.json['data']['object']['id']
        result = OrderService().complete(payload, sig_header, checkout_session_id)
        return result