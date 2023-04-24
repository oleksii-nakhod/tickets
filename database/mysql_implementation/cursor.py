class MysqlCursor():
    def __init__(self, cnxpool, query, vals=None):
        self.cnxpool = cnxpool
        self.query = query
        self.vals = vals

    def __enter__(self):
        self.cnx = self.cnxpool.get_connection()
        self.cur = self.cnx.cursor()
        if self.vals == None:
            self.cur.execute(self.query)
        else:
            self.cur.execute(self.query, self.vals)
        return self.cur
 
    def __exit__(self, *args):
        self.cnx.commit()
        self.cnx.close()