from database.mysql_implementation.user import *
from database.mysql_implementation.user_role import *
from database.mysql_implementation.ticket import *

class MysqlTableList():
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.table_list = {
            'user': MysqlUser,
            'user_role': MysqlUserRole,
            'ticket': MysqlTicket
        }
    
    def get_table(self, table_type):
        table = None
        try:
            table = self.table_list[table_type](self.cnxpool)
        except Exception as e:
            print(e)
        return table
