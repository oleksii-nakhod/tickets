from command.interface.command import *
from service.search import *

class SearchStationsCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        result = SearchService().search_stations(self.request)
        return result