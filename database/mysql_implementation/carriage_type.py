from database.interface.carriage_type import ICarriageType
from database.entity.carriage_type import CarriageType
from database.mysql_implementation.cursor import *

class MysqlCarriageType(ICarriageType):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'carriage_type'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = [CarriageType(*args) for args in cursor.fetchall()]
        return result

    def read(self, id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id={id};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = CarriageType(*cursor.fetchone())
        return result

    
