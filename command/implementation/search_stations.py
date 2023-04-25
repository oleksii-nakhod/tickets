from command.interface.command import *
from service.search import *

class SearchStationsCommand(ICommand):
    def __init__(self, query):
        self.query = query
        
    def execute(self):
        result = SearchService().search_stations(self.query)
        return result