from database.interface.seat import *
from database.entity.seat import *
from database.entity.carriage import *
from database.entity.trip import *
from database.entity.trip_station import *
from database.entity.ticket import *

class MysqlSeat(ISeat):
    def read_all(self, session):
        stmt = select(Seat)
        result = session.scalars(stmt)
        return result

    def read(self, session, id):
        stmt = select(Seat).where(Seat.id == id)
        result = session.scalars(stmt).first()
        return result
    
    def find(self, session, trip, train, ctype, from_station, to_station):
        subquery_carriage = select(Carriage.id).filter(Carriage.carriage_type_id == ctype, Carriage.train_id == (select(Trip.train_id).filter(Trip.id == trip).scalar_subquery()))
        subquery_trip_station = select(TripStation.id).filter(TripStation.trip_id == trip)

        stmt = select(
            Seat.carriage_id,
            func.group_concat(Seat.id),
            func.group_concat(Seat.num)
        ).filter(
            Seat.carriage_id.in_(subquery_carriage),
            Seat.id.notin_(select(Ticket.seat_id).filter(Ticket.trip_station_start_id.in_(subquery_trip_station)))
        ).group_by(
            Seat.carriage_id
        )
        
        data = session.execute(stmt)
        result = []
        for carriage in data:
            obj = {'id': carriage[0], 'seats': []}
            for seat in zip(carriage[1].split(','), carriage[2].split(',')):
                obj['seats'].append({
                    'id': int(seat[0]),
                    'num': int(seat[1])
                })
            result.append(obj)
        return result
