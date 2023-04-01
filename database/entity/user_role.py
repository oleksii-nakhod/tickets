class UserRole():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def print_info(self):
        print(f'User Role #{self.id}\nName: {self.name}\n')
