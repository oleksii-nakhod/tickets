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
        return [ticket.to_dict() for ticket in result]

    def read(self, session, id):
        stmt = select(Ticket).where(Ticket.id == id)
        result = session.scalars(stmt).first()
        return result.to_dict()

    def create(self, session, ticket):
        vals = (ticket.user_id, ticket.seat_id, ticket.trip_station_start_id, ticket.trip_station_end_id, ticket.token)
        stmt = insert(Ticket).values(user_id=ticket.user_id, seat_id=ticket.seat_id, trip_station_start_id=ticket.trip_station_start_id, trip_station_end_id=ticket.trip_station_end_id, token=ticket.token)
        result = session.execute(stmt).inserted_primary_key[0]
        session.commit()
        return {}, 201

    def find(self, session, user_id):
        stmt = select(Ticket).where(Ticket.user_id == user_id)
        result = session.scalars(stmt)
        return [ticket.to_dict() for ticket in result]
    
    def info(self, session, id):
        stmt = select(
            Ticket.id.label('id'),
            Train.name.label('train_name'),
            Carriage.num.label('carriage_num'),
            Seat.num.label('seat_num'),
            Ticket.trip_station_start_id.label('trip_station_start_id'),
            Ticket.trip_station_end_id.label('trip_station_end_id'),
            User.email.label('user_email'),
            User.name.label('user_name')
        ).join(User, User.id == Ticket.user_id).join(Seat, Seat.id == Ticket.seat_id).join(Carriage, Carriage.id == Seat.carriage_id).join(Train, Train.id == Carriage.train_id).filter(
            Ticket.id == id
        )
        result = session.execute(stmt).first()
        return {
            'id': result.id,
            'train_name': result.train_name,
            'carriage_num': result.carriage_num,
            'seat_num': result.seat_num,
            'trip_station_start_id': result.trip_station_start_id,
            'trip_station_end_id': result.trip_station_end_id,
            'user_email': result.user_email,
            'user_name': result.user_name
        }
    
    def verify(self, session, id, token):
        stmt = select(Ticket).where(and_(Ticket.id == id, Ticket.token == token))
        result = session.scalars(stmt).first()
        return result.to_dict()