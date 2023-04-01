class Carriage():
    def __init__(self, id, num, train_id, carriage_type_id):
        self.id = id
        self.num = num
        self.train_id = train_id
        self.carriage_type_id = carriage_type_id

    def print_info(self):
        print(
            f'Carriage #{self.id}\nNum: {self.num}\nTrain ID: {self.train_id}\nCarriage Type ID: {self.carriage_type_id}\n')
