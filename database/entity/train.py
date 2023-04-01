class Train():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def print_info(self):
        print(f'Train #{self.id}\nName: {self.name}\n')
