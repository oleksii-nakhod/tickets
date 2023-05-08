from command.interface.command import *
from service.profile import *

class UpdateProfileCommand(ICommand):
    def __init__(self, request):
        self.request = request
        
    def execute(self):
        fields = self.request.json['fields']
        password = None
        try:
            password = self.request.json['password']
        except:
            pass
        result = ProfileService().update(fields, password)
        return result