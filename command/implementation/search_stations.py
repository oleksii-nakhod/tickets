from command.interface.command import *
from service.search import *

class SearchStationsCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        query = self.request.args.get('q')
        result = SearchService().search_stations(query)
        return result