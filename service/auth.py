from flask import current_app, session, redirect, url_for
from database.mysql_implementation.user import *

class AuthService:
    def login(self, email, password):
        try:
            engine = current_app.config['engine']
            user_table = current_app.config['tables']['user']
            with Session(engine) as s:
                user = user_table.find(s, email, password)
                if user:
                    session['logged_in'] = True
                    session['id'] = user.id
                    session['email'] = user.email
                    session['name'] = user.name
                    session['user_role_id'] = user.user_role_id
                    return {'msg': 'Success'}, 200
                else:
                    return {'msg': 'Incorrect email/password'}, 401
        except Exception as e:
            print(e)
        return {'msg': 'Server Error'}, 500
    
    def signup(self, name, email, password):
        try:
            engine = current_app.config['engine']
            user_table = current_app.config['tables']['user']
            with Session(engine) as s:
                user = user_table.find(s, email)
                if user:
                    return {'msg': 'This email address is already registered. If that\'s you, please log in instead.'}, 409
                else:
                    user_id = user_table.create(s, User(
                        name=name,
                        email=email,
                        user_role_id=2
                    ), password)
                    session['logged_in'] = True
                    session['id'] = user_id
                    session['email'] = email
                    session['name'] = name
                    session['user_role_id'] = 2
                    return {'msg': 'success'}, 200
        except Exception as e:
            print(e)
        return {'msg': 'server error'}, 500
    
    def logout(self):
        session.clear()
        return redirect(url_for('index'))
    