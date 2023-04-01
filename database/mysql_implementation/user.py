from database.interface.user import IUser
from database.entity.user import User

class MysqlUser(IUser):
    def __init__(self, cnxpool):
        self.cnxpool = cnxpool
        self.tname = 'user'

    def read_all(self):
        result = None
        query = f"SELECT * FROM {self.tname};"
        try:
            self.cnx = self.cnxpool.get_connection()
            self.cur = self.cnx.cursor()
            self.cur.execute(query)
            result = [User(*args) for args in self.cur.fetchall()]
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
            result = User(*self.cur.fetchone())
            self.cnx.close()
        except Exception as e:
            print(e)
        return result

    def create(self, user):
        result = None
        vals = (user.name, user.email, user.password_hash, user.user_role_id)
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