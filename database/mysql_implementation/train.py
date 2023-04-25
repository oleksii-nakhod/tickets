from database.interface.train import ITrain
from database.entity.train import Train
from database.mysql_implementation.cursor import *

class MysqlTrain(ITrain):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'train'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = [Train(*args) for args in cursor.fetchall()]
        return result

    def read(self, id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id={id};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            args = cursor.fetchone()
            if args:
                result = Train(*args)
        return result

    def find(self, trip_id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id=(SELECT train_id FROM trip WHERE id={trip_id});"
        with MysqlCursor(self.cnxpool, query) as cursor:
            args = cursor.fetchone()
            if args:
                result = Train(*args)
        return result

    
