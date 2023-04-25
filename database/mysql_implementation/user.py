from database.interface.user import IUser
from database.entity.user import User
from database.mysql_implementation.cursor import *
import bcrypt

class MysqlUser(IUser):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'user'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            result = [User(*args) for args in cursor.fetchall()]
        return result

    def read(self, id):
        result = None
        query = f"SELECT * FROM {self.tname} WHERE id={id};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            args = cursor.fetchone()
            if args:
                result = User(*args)
        return result

    def create(self, user, password):
        result = None
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        vals = (user.name, user.email, password_hash, user.user_role_id)
        query = f"INSERT INTO {self.tname} ( \
                    name, \
                    email, \
                    password_hash, \
                    user_role_id \
                ) \
                VALUES ( \
                    %s, \
                    %s, \
                    %s, \
                    %s \
                )"
        with MysqlCursor(self.cnxpool, query, vals) as cursor:
            result = cursor.lastrowid
        return result

    def update(self, id, fields):
        vals = []
        for key in fields:
            if key == 'password':
                password = fields[key]
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
                vals.append(f"password_hash = '{password_hash.decode('utf-8')}'")
            else:
                vals.append(f"{key} = '{fields[key]}'")
        vals = ', '.join(vals)
        query = f"UPDATE {self.tname} SET {vals} WHERE id={id};"
        with MysqlCursor(self.cnxpool, query) as cursor:
            pass

    def delete(self, id):
        query = f"DELETE FROM {self.tname} WHERE id={id}"
        with MysqlCursor(self.cnxpool, query) as cursor:
            pass
            
    def find(self, email, password=None):
        result = []
        query = f"SELECT * FROM {self.tname} WHERE email='{email}';"
        with MysqlCursor(self.cnxpool, query) as cursor:
            args = cursor.fetchone()
            if args:
                user = User(*args)
            else:
                return result
            if (password == None or bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))):
                result = user
        return result
