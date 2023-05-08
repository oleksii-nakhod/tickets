from command.interface.command import *
from service.search import *

class SearchTicketsCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        from_station = self.request.args.get('from')
        to_station = self.request.args.get('to')
        depart_date = self.request.args.get('depart')
        result = SearchService().search_tickets(from_station, to_station, depart_date)
        return result