from command.interface.command import *
from service.profile import *

class ReadProfileCommand(ICommand):
    def __init__(self):
        pass
        
    def execute(self):
        result = ProfileService().read()
        return result