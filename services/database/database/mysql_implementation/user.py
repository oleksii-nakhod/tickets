from database.interface.user import *
from database.entity.user import *
import bcrypt

class MysqlUser(IUser):
    def read_all(self, session):
        stmt = select(User)
        result = session.scalars(stmt)
        return [user.to_dict() for user in result]

    def read(self, session, id):
        stmt = select(User).where(User.id == id)
        result = session.scalars(stmt).first()
        return result.to_dict()

    def create(self, session, user, password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        stmt = insert(User).values(name=user.name, email=user.email, password_hash=password_hash, user_role_id=user.user_role_id, confirm_email_token=user.confirm_email_token)
        user = session.execute(stmt).inserted_primary_key[0]
        session.commit()
        return {"id": user}, 201

    def update(self, session, id, fields):
        vals = {}
        for key, value in fields.items():
            if key == 'password':
                password = value
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
                vals['password_hash'] = password_hash.decode('utf-8')
            else:
                vals[key] = value
        
        stmt = update(User).where(User.id == id).values(vals)
        session.execute(stmt)
        session.commit()
        return {}, 200
            
    def find(self, session, email, password=None):
        stmt = select(User).where(User.email == email)
        user = session.scalars(stmt).first()
        if not user:
            return []
        if not password:
            return [user.to_dict()]
        if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return [user.to_dict()]
        return []
