class Trip():
    def __init__(self, id, train_id):
        self.id = id
        self.train_id = train_id

    def print_info(self):
        print(f'Trip #{self.id}\nTrain ID: {self.train_id}\n')
