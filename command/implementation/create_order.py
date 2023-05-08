from command.interface.command import *
from service.order import *

class CreateOrderCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        station_start_id = self.request.json['station_start_id']
        station_end_id = self.request.json['station_end_id']
        trip_id = self.request.json['trip_id']
        seats = self.request.json['seats']
        result = OrderService().create(station_start_id, station_end_id, trip_id, seats)
        return result