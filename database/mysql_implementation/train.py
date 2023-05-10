from database.interface.train import *
from database.entity.train import *
from database.entity.trip import *

class MysqlTrain(ITrain):
    def read_all(self, session):
        stmt = select(Train)
        result = session.scalars(stmt)
        return result

    def read(self, session, id):
        stmt = select(Train).where(Train.id == id)
        result = session.scalars(stmt).first()
        return result

    def find(self, session, trip_id):
        subq = select(Trip.train_id).where(Trip.id == trip_id).scalar_subquery()
        stmt = select(Train).where(Train.id == subq)
        result = session.scalars(stmt).first()
        return result

    
