from database.interface.station import *
from database.entity.station import *

class MysqlStation(IStation):
    def read_all(self, session):
        stmt = select(Station)
        result = session.scalars(stmt)
        return [station.to_dict() for station in result]

    def read(self, session, id):
        stmt = select(Station).where(Station.id == id)
        result = session.scalars(stmt).first()
        return result.to_dict()

    def find(self, session, query):
        stmt = select(Station).where(Station.name.like(f"{query}%"))
        result = session.scalars(stmt)
        return [station.to_dict() for station in result]

