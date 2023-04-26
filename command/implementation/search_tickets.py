from command.interface.command import *
from service.search import *

class SearchTicketsCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        result = SearchService().search_tickets(self.request)
        return result