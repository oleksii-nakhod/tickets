from database.interface.ticket import ITicket
from database.entity.ticket import Ticket


class MysqlTicket(ITicket):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'ticket'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            result = [Ticket(*args) for args in self.cur.fetchall()]
            self.cnx.close()
        except Exception as e:
            print(e)
        return result

    def read(self, id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id={id};"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            result = Ticket(*self.cur.fetchone())
            self.cnx.close()
        except Exception as e:
            print(e)
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
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query, vals)
            self.cnx.commit()
            result = self.cur.lastrowid
            self.cnx.close()
        except Exception as e:
            print(e)
        return result

    def find(self, user_id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE user_id = {user_id}"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            result = [Ticket(*args) for args in self.cur.fetchall()]
            print(result)
            self.cnx.close()
        except Exception as e:
            print(e)
        return result
    
    def verify(self, id, token):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id = {id} AND token = '{token}'"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            print(query)
            result = Ticket(*self.cur.fetchone())
            print(result)
            self.cnx.close()
        except Exception as e:
            print(e)
        return result
