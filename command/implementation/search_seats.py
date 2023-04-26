from command.interface.command import *
from service.search import *

class SearchSeatsCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        result = SearchService().search_seats(self.request)
        return result