from database.interface.carriage_type import ICarriageType
from database.entity.carriage_type import CarriageType


class MysqlCarriageType(ICarriageType):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'carriage_type'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            result = [CarriageType(*args) for args in self.cur.fetchall()]
            self.cnx.close()
        except Exception as e:
            print(e)
        return result

    def read(self, id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id={id};"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            result = CarriageType(*self.cur.fetchone())
            self.cnx.close()
        except Exception as e:
            print(e)
        return result

    
