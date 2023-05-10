from database.interface.carriage import *
from database.entity.carriage import *
from database.entity.carriage_type import *
from database.entity.seat import *

class MysqlCarriage(ICarriage):
    def read_all(self, session):
        stmt = select(Carriage)
        result = session.scalars(stmt)
        return result

    def read(self, session, id):
        stmt = select(Carriage).where(Carriage.id == id)
        result = session.scalars(stmt).first()
        return result
    
    def find(self, session, trip_id):
        # stmt = select([CarriageType.c.id, CarriageType.c.name, CarriageType.c.price_mod, text('count(*)')]).select_from(Seat.join(Carriage, Seat.c.carriage_id == Carriage.c.id).join(CarriageType, Carriage.c.carriage_type_id == CarriageType.c.id)).where(text('carriage_id'))
        query = f"SELECT carriage_type.id, carriage_type.name, carriage_type.price_mod, count(*) FROM seat JOIN carriage ON seat.carriage_id = carriage.id JOIN carriage_type ON carriage.carriage_type_id = carriage_type.id WHERE carriage_id in (SELECT id FROM carriage WHERE train_id = (SELECT train_id FROM trip WHERE id = {trip_id})) AND seat.id NOT IN (SELECT seat_id FROM ticket WHERE trip_station_start_id IN (SELECT id FROM trip_station WHERE trip_id = {trip_id})) GROUP BY carriage_type.id, carriage_type.name;"
        stmt = text(query)
        result = session.execute(stmt)
        return result
    
