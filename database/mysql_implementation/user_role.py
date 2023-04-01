from database.interface.user_role import *
from database.entity.user_role import UserRole

class MysqlUserRole(IUserRole):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'user_role'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            result = [UserRole(*args) for args in self.cur.fetchall()]
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
            result = UserRole(*self.cur.fetchone())
            self.cnx.close()
        except Exception as e:
            print(e)
        return result

    def create(self, user_role):
        result = None
        vals = (user_role.name)
        query = f"INSERT INTO {self.tname} ( \
                    name \
                ) \
                VALUES ( \
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
