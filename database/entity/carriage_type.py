class CarriageType():
    def __init__(self, id, name, price_mod):
        self.id = id
        self.name = name
        self.price_mod = price_mod

    def print_info(self):
        print(
            f'Carriage Type #{self.id}\nName: {self.name}\nPrice Modifier: {self.price_mod}\n')
