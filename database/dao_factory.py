from database.mysql_dao_factory import *

class DatabaseList():
    def __init__(self):
        self.db_list = {
            'mysql': MysqlTableList
        }

    def get_database(self, db_type):
        db = None
        try:
            db = self.db_list[db_type]()
        except Exception as e:
            print(e)
        return db
