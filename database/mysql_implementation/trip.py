from database.interface.trip import *
from database.entity.trip import *

class MysqlTrip(ITrip):
    def read_all(self, session):
        stmt = select(Trip)
        result = session.scalars(stmt)
        return result

    def read(self, session, id):
        stmt = select(Trip).where(Trip.id == id)
        result = session.scalars(stmt).one()
        return result
    
    def find(self, station_start, station_end, depart_date):
        result = None
        query = f'SELECT t1.trip_id, t1.time_dep, t2.time_arr, t2.price-t1.price FROM trip_station t1, trip_station t2 WHERE t1.station_id = {station_start} AND t2.station_id = {station_end} AND t1.trip_id = t2.trip_id AND t1.num < t2.num AND DATE(t1.time_dep) = "{depart_date}" GROUP BY t1.trip_id, t1.time_dep, t2.time_arr, t1.price, t2.price;'
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = cursor.fetchall()
        return result
    
    def find_seats(self, trip_id):
        result = None
        query = f"SELECT carriage_type.id, carriage_type.name, carriage_type.price_mod, count(*) FROM seat JOIN carriage ON seat.carriage_id = carriage.id JOIN carriage_type ON carriage.carriage_type_id = carriage_type.id WHERE carriage_id in (SELECT id FROM carriage WHERE train_id = (SELECT train_id FROM trip WHERE id = {trip_id})) GROUP BY carriage_type.id, carriage_type.name;"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = cursor.fetchall()
        return result

    
