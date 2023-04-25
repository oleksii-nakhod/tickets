from command.interface.command import *
from service.search import *

class SearchTicketsCommand(ICommand):
    def __init__(self, from_station, to_station, depart_date):
        self.from_station = from_station
        self.to_station = to_station
        self.depart_date = depart_date
        
    def execute(self):
        result = SearchService().search_tickets(self.from_station, self.to_station, self.depart_date)
        return result