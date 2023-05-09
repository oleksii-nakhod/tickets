from database.interface.train import *
from database.entity.train import *

class MysqlTrain(ITrain):
    def read_all(self, session):
        stmt = select(Train)
        result = session.scalars(stmt)
        return result

    def read(self, session, id):
        stmt = select(Train).where(Train.id == id)
        result = session.scalars(stmt).one()
        return result

    def find(self, trip_id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id=(SELECT train_id FROM trip WHERE id={trip_id});"
        with MysqlCursor(self.cnxpool, query) as cursor:
            args = cursor.fetchone()
            if args:
                result = Train(*args)
        return result

    
