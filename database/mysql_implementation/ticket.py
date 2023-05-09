from database.interface.ticket import *
from database.entity.ticket import *

class MysqlTicket(ITicket):
    def read_all(self, session):
        stmt = select(Ticket)
        result = session.scalars(stmt)
        return result

    def read(self, session, id):
        stmt = select(Ticket).where(Ticket.id == id)
        result = session.scalars(stmt).one()
        return result

    def create(self, ticket):
        result = None
        vals = (ticket.user_id, ticket.seat_id, ticket.trip_station_start_id, ticket.trip_station_end_id, ticket.token)
        query = f"INSERT INTO {self.tname} ( \
                    user_id, \
                    seat_id, \
                    trip_station_start_id, \
                    trip_station_end_id, \
                    token \
                ) \
                VALUES ( \
                    %s, \
                    %s, \
                    %s, \
                    %s, \
                    %s \
                )"
        with MysqlCursor(self.cnxpool, query, vals) as cursor:
            result = cursor.lastrowid
        return result

    def find(self, user_id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE user_id = {user_id}"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = [Ticket(*args) for args in cursor.fetchall()]
        return result
    
    def info(self, id):
        result = None
        query = f"SELECT ticket.id as id, train.name as train_name, carriage.num as carriage_num, seat.num as seat_num, ticket.trip_station_start_id as trip_station_start_id, ticket.trip_station_end_id as trip_station_end_id, user.email as user_email FROM ticket JOIN user ON user.id = ticket.user_id JOIN seat ON seat.id = ticket.seat_id JOIN carriage ON carriage.id = seat.carriage_id JOIN train ON train.id = carriage.train_id WHERE ticket.id={id}"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = cursor.fetchone()
        return result
    
    def verify(self, id, token):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id = {id} AND token = '{token}'"
        with MysqlCursor(self.cnxpool, query) as cursor:
            args = cursor.fetchone()
            if args:
                result = Ticket(*args)
        return result
