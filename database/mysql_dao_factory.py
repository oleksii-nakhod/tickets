from database.mysql_implementation import *

class MysqlTableList():
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.table_list = {
            'carriage': MysqlCarriage,
            'carriage_type': MysqlCarriageType,
            'seat': MysqlSeat,
            'station': MysqlStation,
            'ticket': MysqlTicket,
            'train': MysqlTrain,
            'trip': MysqlTrip,
            'trip_station': MysqlTripStation,
            'user': MysqlUser,
            'user_role': MysqlUserRole,
            
        }
    
    def get_table(self, table_type):
        table = None
        try:
            table = self.table_list[table_type](self.cnxpool)
        except Exception as e:
            print(e)
        return table
