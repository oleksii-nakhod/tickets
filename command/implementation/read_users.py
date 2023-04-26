from command.interface.command import *
from service.admin import *

class ReadUsersCommand(ICommand):
    def __init__(self):
        pass
        
    def execute(self):
        result = AdminService().read_users()
        return result