class User():
    def __init__(self, id=None, name=None, email=None, password_hash=None, user_role_id=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.user_role_id = user_role_id
    
    def print_info(self):
        print(f'User #{self.id}\nName: {self.name}\nEmail: {self.email}\nPassword hash: {self.password_hash}\nUser type ID: {self.user_role_id}\n')