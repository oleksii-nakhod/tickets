from database.interface.station import IStation
from database.entity.station import Station

class MysqlStation(IStation):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'station'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            result = [Station(*args) for args in self.cur.fetchall()]
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
            result = Station(*self.cur.fetchone())
            self.cnx.close()
        except Exception as e:
            print(e)
        return result

    def find(self, query):
        result = []
        query = f"SELECT * FROM {self.tname} WHERE name LIKE '{query}%';"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            result = [Station(*args) for args in self.cur.fetchall()]
            self.cnx.close()
        except Exception as e:
            print(e)
        return result

