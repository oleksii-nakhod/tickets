from database.interface.carriage_type import *
from database.entity.carriage_type import *

class MysqlCarriageType(ICarriageType):
    def read_all(self, session):
        stmt = select(CarriageType)
        result = session.scalars(stmt)
        return [carriage_type.to_dict() for carriage_type in result]

    def read(self, session, id):
        stmt = select(CarriageType).where(CarriageType.id == id)
        result = session.scalars(stmt).first()
        return result.to_dict()

    
