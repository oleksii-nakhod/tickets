from database.interface.trip_station import ITripStation
from database.entity.trip_station import TripStation
from database.mysql_implementation.cursor import *

class MysqlTripStation(ITripStation):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'trip_station'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = [TripStation(*args) for args in cursor.fetchall()]
        return result

    def read(self, id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id={id};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = TripStation(*cursor.fetchone())
        return result
    
    def find(self, trip_id, station_start, station_end):
        result = None
        query = f"SELECT t1.time_dep, t2.time_arr, t2.price - t1.price FROM trip_station t1, trip_station t2 WHERE t1.station_id = {station_start} AND t2.station_id = {station_end} AND t1.trip_id = {trip_id} AND t2.trip_id = {trip_id}"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = cursor.fetchone()
        return result
    

    
