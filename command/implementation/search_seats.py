from command.interface.command import *
from service.search import *

class SearchSeatsCommand(ICommand):
    def __init__(self, trip, ctype, from_station, to_station):
        self.trip = trip
        self.ctype = ctype
        self.from_station = from_station
        self.to_station = to_station
        
    def execute(self):
        result = SearchService().search_seats(self.trip, self.ctype, self.from_station, self.to_station)
        return result