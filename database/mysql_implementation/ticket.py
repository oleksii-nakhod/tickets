from database.interface.ticket import *
from database.entity.ticket import *
from database.entity.train import *
from database.entity.carriage import *
from database.entity.seat import *
from database.entity.user import *

class MysqlTicket(ITicket):
    def read_all(self, session):
        stmt = select(Ticket)
        result = session.scalars(stmt)
        return result

    def read(self, session, id):
        stmt = select(Ticket).where(Ticket.id == id)
        result = session.scalars(stmt).first()
        return result

    def create(self, session, ticket):
        vals = (ticket.user_id, ticket.seat_id, ticket.trip_station_start_id, ticket.trip_station_end_id, ticket.token)
        stmt = insert(Ticket).values(user_id=ticket.user_id, seat_id=ticket.seat_id, trip_station_start_id=ticket.trip_station_start_id, trip_station_end_id=ticket.trip_station_end_id, token=ticket.token)
        session.execute(stmt)
        session.commit()

    def find(self, session, user_id):
        stmt = select(Ticket).where(Ticket.user_id == user_id)
        result = session.scalars(stmt)
        return result
    
    def info(self, session, id):
        # stmt = select([Ticket.c.id.label('id'), Train.c.name.label('train_name'), Carriage.c.num.label('carriage_num'), Seat.c.num.label('seat_num'), Ticket.c.trip_station_start_id.label('trip_station_start_id'), Ticket.c.trip_station_end_id.label('trip_station_end_id'), User.c.email.label('user_email')]).select_from(Ticket.join(User, user.c.id == Ticket.c.user_id).join(Seat, Seat.c.id == Ticket.c.seat_id).join(Carriage, Carriage.c.id == Seat.c.carriage_id).join(Train, Train.c.id == Carriage.c.train_id)).where(Ticket.c.id)
        query = f"SELECT ticket.id as id, train.name as train_name, carriage.num as carriage_num, seat.num as seat_num, ticket.trip_station_start_id as trip_station_start_id, ticket.trip_station_end_id as trip_station_end_id, user.email as user_email FROM ticket JOIN user ON user.id = ticket.user_id JOIN seat ON seat.id = ticket.seat_id JOIN carriage ON carriage.id = seat.carriage_id JOIN train ON train.id = carriage.train_id WHERE ticket.id={id}"
        stmt = text(query)
        result = session.execute(stmt).first()
        return result
    
    def verify(self, session, id, token):
        stmt = select(Ticket).where(and_(Ticket.id == id, Ticket.token == token))
        result = session.scalars(stmt).first()
        return result