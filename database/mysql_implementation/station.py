from database.interface.station import IStation
from database.entity.station import Station
from database.mysql_implementation.cursor import *

class MysqlStation(IStation):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'station'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = [Station(*args) for args in cursor.fetchall()]
        return result

    def read(self, id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id={id};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            args = cursor.fetchone()
            if args:
                result = Station(*args)
        return result

    def find(self, query):
        result = []
        query = f"SELECT * FROM {self.tname} WHERE name LIKE '{query}%';"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = [Station(*args) for args in cursor.fetchall()]
        return result

