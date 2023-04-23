from database.interface.train import ITrain
from database.entity.train import Train


class MysqlTrain(ITrain):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'train'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            result = [Train(*args) for args in self.cur.fetchall()]
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
            result = Train(*self.cur.fetchone())
            self.cnx.close()
        except Exception as e:
            print(e)
        return result

    
