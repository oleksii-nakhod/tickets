from database.interface.trip_station import *
from database.entity.trip_station import *

class MysqlTripStation(ITripStation):
    def read_all(self, session):
        stmt = select(TripStation)
        result = session.scalars(stmt)
        return [trip_station.to_dict() for trip_station in result]

    def read(self, session, id):
        stmt = select(TripStation).where(TripStation.id == id)
        result = session.scalars(stmt).first()
        return result.to_dict()
    
    def info(self, session, trip_id, station_start, station_end):
        t1 = aliased(TripStation)
        t2 = aliased(TripStation)
        stmt = select(t1.time_dep, t2.time_arr, t2.price - t1.price).select_from(join(t1, t2, t1.trip_id == t2.trip_id)).where(and_(t1.station_id == station_start, t2.station_id == station_end, t1.trip_id == trip_id, t2.trip_id == trip_id))
        result = session.execute(stmt).first()
        import logging
        logger = logging.getLogger(__name__)
        logger.info(result)
        return {
            'time_dep': result[0].isoformat() + 'Z',
            'time_arr': result[1].isoformat() + 'Z',
            'price': result[2]
        }
    
    def find(self, session, trip_id, station_id):
        stmt = select(TripStation).where(TripStation.trip_id == trip_id, TripStation.station_id == station_id)
        result = session.scalars(stmt).first()
        if result is None:
            return []
        return [result.to_dict()]
    

    
