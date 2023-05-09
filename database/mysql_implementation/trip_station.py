from database.interface.trip_station import *
from database.entity.trip_station import *

class MysqlTripStation(ITripStation):
    def read_all(self, session):
        stmt = select(TripStation)
        result = session.scalars(stmt)
        return result

    def read(self, session, id):
        stmt = select(TripStation).where(TripStation.id == id)
        result = session.scalars(stmt).one()
        return result
    
    def find(self, trip_id, station_start, station_end):
        result = None
        query = f"SELECT t1.time_dep, t2.time_arr, t2.price - t1.price FROM trip_station t1, trip_station t2 WHERE t1.station_id = {station_start} AND t2.station_id = {station_end} AND t1.trip_id = {trip_id} AND t2.trip_id = {trip_id}"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = cursor.fetchone()
        return result
    

    
