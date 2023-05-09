from database.interface.station import *
from database.entity.station import *

class MysqlStation(IStation):
    def read_all(self, session):
        stmt = select(Station)
        result = session.scalars(stmt)
        return result

    def read(self, session, id):
        stmt = select(Station).where(Station.id == id)
        result = session.scalars(stmt).one()
        return result

    def find(self, session, query):
        stmt = select(Station).where(Station.name.like(f"{query}%"))
        result = session.scalars(stmt)
        print(result)
        return result

