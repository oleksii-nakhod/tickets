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
        vals = (ticket.user_id, ticket.seat_id, ticket.trip_station_start_id, ticket.trip_station_end_id)
        query = f"INSERT INTO {self.tname} ( \
                    user_id, \
                    seat_id, \
                    trip_station_start_id, \
                    trip_station_end_id \
                ) \
                VALUES ( \
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

    def update(self, id, fields):
        vals = []
        for key in fields:
            vals.append(f"{key} = '{fields[key]}'")
        vals = ', '.join(vals)
        query = f"UPDATE {self.tname} SET {vals} WHERE id={id};"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            self.cnx.commit()
            self.cnx.close()
        except Exception as e:
            print(e)

    def delete(self, id):
        query = f"DELETE FROM {self.tname} WHERE id={id}"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            self.cnx.commit()
            self.cnx.close()
        except Exception as e:
            print(e)
