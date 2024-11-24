from database.interface.carriage import *
from database.entity.carriage import *
from database.entity.carriage_type import *
from database.entity.seat import *
from database.entity.trip import *
from database.entity.ticket import *
from database.entity.trip_station import *

class MysqlCarriage(ICarriage):
    def read_all(self, session):
        stmt = select(Carriage)
        result = session.scalars(stmt)
        return [carriage.to_dict() for carriage in result]

    def read(self, session, id):
        stmt = select(Carriage).where(Carriage.id == id)
        result = session.scalars(stmt).first()
        return result.to_dict()
    
    def find(self, session, trip_id):
        subquery_carriage = select(Carriage.id).filter(Carriage.train_id == (select(Trip.train_id).filter(Trip.id == trip_id).scalar_subquery()))
        
        subquery_trip_station = select(TripStation.id).filter(TripStation.trip_id == trip_id)

        stmt = select(
            CarriageType.id,
            CarriageType.name,
            CarriageType.price_mod,
            func.count()
        ).join(Seat.carriage).join(CarriageType).filter(
            Carriage.id.in_(subquery_carriage),
            Seat.id.notin_(select(Ticket.seat_id).filter(Ticket.trip_station_start_id.in_(subquery_trip_station)))
        ).group_by(
            CarriageType.id,
            CarriageType.name
        )
        
        result = session.execute(stmt)
        return [{
            'carriage_type_id': row.id,
            'carriage_type_name': row.name,
            'price_mod': row.price_mod,
            'count': row.count
        } for row in result]
    
