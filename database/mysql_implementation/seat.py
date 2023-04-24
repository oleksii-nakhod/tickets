from database.interface.seat import ISeat
from database.entity.seat import Seat
from database.mysql_implementation.cursor import *

class MysqlSeat(ISeat):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'seat'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = [Seat(*args) for args in cursor.fetchall()]
        return result

    def read(self, id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id={id};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = Seat(*cursor.fetchone())
        return result
    
    def find(self, trip, train, ctype, from_station, to_station):
        result = None
        query = f"SELECT carriage_id, GROUP_CONCAT(id), GROUP_CONCAT(num) FROM seat WHERE carriage_id IN(SELECT id FROM carriage WHERE carriage_type_id={ctype} AND train_id=(SELECT train_id FROM trip WHERE id={trip})) GROUP BY carriage_id;"
        with MysqlCursor(self.cnxpool, query) as cursor:
            data = cursor.fetchall()
            result = []
            for carriage in data:
                obj = {'id': carriage[0], 'seats': []}
                for seat in zip(carriage[1].split(','), carriage[2].split(',')):
                    obj['seats'].append({
                        'id': int(seat[0]),
                        'num': int(seat[1])
                    })
                result.append(obj)
        return result

    
    
