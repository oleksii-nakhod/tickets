from database.interface.trip import *
from database.entity.trip import *
from database.entity.trip_station import *

class MysqlTrip(ITrip):
    def read_all(self, session):
        stmt = select(Trip)
        result = session.scalars(stmt)
        return [trip.to_dict() for trip in result]

    def read(self, session, id):
        stmt = select(Trip).where(Trip.id == id)
        result = session.scalars(stmt).first()
        return result.to_dict()
    
    def find(self, session, station_start, station_end, depart_date):
        t1 = aliased(TripStation)
        t2 = aliased(TripStation)
        
        stmt = select(
            t1.trip_id,
            t1.time_dep,
            t2.time_arr,
            (t2.price - t1.price).label('price_difference')
        ).join(
            t2,
            (t1.station_id == station_start) &
            (t2.station_id == station_end) &
            (t1.trip_id == t2.trip_id) &
            (t1.num < t2.num) &
            (func.date(t1.time_dep) == depart_date)
        ).group_by(
            t1.trip_id,
            t1.time_dep,
            t2.time_arr,
            t1.price,
            t2.price
        )

        result = session.execute(stmt)
        return [{
            'id': row.trip_id,
            'time_dep': row.time_dep.isoformat() + 'Z',
            'time_arr': row.time_arr.isoformat() + 'Z',
            'price': row.price_difference
        } for row in result]

    
