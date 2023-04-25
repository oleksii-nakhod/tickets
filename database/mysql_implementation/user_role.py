from database.interface.user_role import *
from database.entity.user_role import UserRole
from database.mysql_implementation.cursor import *

class MysqlUserRole(IUserRole):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'user_role'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = [UserRole(*args) for args in cursor.fetchall()]
        return result

    def read(self, id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id={id};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            args = cursor.fetchone()
            if args:
                result = UserRole(*args)
        return result
