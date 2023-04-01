import mysql.connector
from connection.cnxpool_interface import *


class MysqlConnectionPool(IConnectionPool):
    def __init__(self, pool_name="pool", pool_size=10,  pool_reset_session=True, cnxpool_config={}):
        self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=pool_name, pool_size=pool_size,  pool_reset_session=pool_reset_session, **cnxpool_config)

    def add_connection(self, cnx):
        try:
            self.cnxpool.add_connection(cnx)
        except Exception as e:
            print(e)

    def get_connection(self):
        cnx = None
        try:
            cnx = self.cnxpool.get_connection()
        except Exception as e:
            print(e)
        return cnx
