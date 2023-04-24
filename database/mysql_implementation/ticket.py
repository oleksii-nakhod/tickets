from database.interface.ticket import ITicket
from database.entity.ticket import Ticket
from database.mysql_implementation.cursor import *

class MysqlTicket(ITicket):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'ticket'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = [Ticket(*args) for args in cursor.fetchall()]
        
        return result

    def read(self, id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id={id};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = Ticket(*cursor.fetchone())
        return result

    def create(self, ticket):
        result = None
        vals = (ticket.user_id, ticket.seat_id, ticket.trip_station_start_id, ticket.trip_station_end_id, ticket.token)
        print(vals)
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
    
    def verify(self, id, token):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id = {id} AND token = '{token}'"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = Ticket(*cursor.fetchone())
        return result
