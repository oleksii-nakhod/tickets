import os
from dotenv import load_dotenv
from connection.cnxpool_factory import ConnectionPoolList
from database.dao_factory import DatabaseList
from database.entity.user import User

load_dotenv()

cnxpool_config = {
    "host": os.getenv('HOST'),
    "database": os.getenv('DATABASE'),
    "user": os.getenv('USER'),
    "password": os.getenv('PASSWORD')
}

database_type = os.getenv('DATABASE_TYPE')

cnxpool = ConnectionPoolList().get_cnxpool(database_type, cnxpool_config)

database = DatabaseList().get_database(database_type, cnxpool)


users = database.get_table('user')
user_list = users.read_all()
print("All User records:")
for user in user_list:
    user.print_info()
    

user_roles = database.get_table('user_role')
user_role_list = user_roles.read_all()
print("All User Roles records:")
for user_role in user_role_list:
    user_role.print_info()
    

new_user_id = users.create(User(
    name='Oleksii2',
    email='nakhod.oleksii@lll.kpi.ua',
    password_hash='$2y$10$1FVZyP50I7YrEcEcpnAvPOWnIwHXyAsvw3THYhmsEsXKkWOnYHAGa',
    user_role_id=2
))
print("Created User:")
users.read(id=new_user_id).print_info()


users.update(id=1, fields={'name': 'Oleksii3', 'email': 'example@example.com'})
print("Modified User:")
users.read(id=1).print_info()


users.delete(id=2)
user_list = users.read_all()
print("All User records:")
for user in user_list:
    user.print_info()