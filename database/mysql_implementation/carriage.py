from database.interface.carriage import ICarriage
from database.entity.carriage import Carriage
from database.mysql_implementation.cursor import *

class MysqlCarriage(ICarriage):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'carriage'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = [Carriage(*args) for args in cursor.fetchall()]
        return result

    def read(self, id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id={id};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = Carriage(*cursor.fetchone())
        return result
    
    def find(self, trip_id):
        result = None
        query = f"SELECT carriage_type.id, carriage_type.name, carriage_type.price_mod, count(*) FROM seat JOIN carriage ON seat.carriage_id = carriage.id JOIN carriage_type ON carriage.carriage_type_id = carriage_type.id WHERE carriage_id in (SELECT id FROM carriage WHERE train_id = (SELECT train_id FROM trip WHERE id = {trip_id})) GROUP BY carriage_type.id, carriage_type.name;"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = cursor.fetchall()
        return result

    
