from database.interface.seat import *
from database.entity.seat import *

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
        result = None
        query = f"SELECT carriage_id, GROUP_CONCAT(id), GROUP_CONCAT(num) FROM seat WHERE carriage_id IN(SELECT id FROM carriage WHERE carriage_type_id={ctype} AND train_id=(SELECT train_id FROM trip WHERE id={trip})) AND seat.id NOT IN (SELECT seat_id FROM ticket WHERE trip_station_start_id IN (SELECT id FROM trip_station WHERE trip_id = 1)) GROUP BY carriage_id;"
        stmt = text(query)
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
