from database.interface.user_role import *
from database.entity.user_role import *

class MysqlUserRole(IUserRole):
    def read_all(self):
        stmt = select(UserRole)
        result = session.scalars(stmt)
        return result

    def read(self, id):
        stmt = select(UserRole).where(UserRole.id == id)
        result = session.scalars(stmt).one()
        return result
