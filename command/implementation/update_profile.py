from command.interface.command import *
from service.profile import *

class UpdateProfileCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        result = ProfileService().update(self.request)
        return result