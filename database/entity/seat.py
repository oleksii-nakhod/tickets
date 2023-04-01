class Seat():
    def __init__(self, id=None, num=None, carriage_id=None):
        self.id = id
        self.num = num
        self.carriage_id = carriage_id

    def print_info(self):
        print(f'Seat #{self.id}\nNum: {self.num}\nCarriage ID: {self.carriage_id}\n')
