from command.interface.command import *
from service.search import *

class SearchSeatsCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        trip = self.request.args.get('trip')
        ctype = self.request.args.get('ctype')
        from_station = self.request.args.get('from')
        to_station = self.request.args.get('to')
        result = SearchService().search_seats(trip, ctype, from_station, to_station)
        return result