from connection.mysql_cnxpool import *


class ConnectionPoolList():
    def __init__(self):
        self.cnxpool_list = {
            'mysql': MysqlConnectionPool
        }

    def get_cnxpool(self, db_type, cnxpool_config):
        return self.cnxpool_list[db_type](cnxpool_config=cnxpool_config)
