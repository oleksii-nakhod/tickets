from flask import current_app, session, redirect, url_for
from database.mysql_implementation.user import *
import random
import os
import string
from service.mail import *

class AuthService:
    def login(self, email, password):
        try:
            engine = current_app.config['engine']
            user_table = current_app.config['tables']['user']
            with Session(engine) as s:
                user = user_table.find(s, email, password)
                if user:
                    if not user.confirmed_email:
                        return {'msg': 'Please confirm your email before logging in'}, 401
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
                    confirm_email_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    user_id = user_table.create(s, User(
                        name=name,
                        email=email,
                        user_role_id=2,
                        confirm_email_token=confirm_email_token
                    ), password)
                    
                    dynamic_template_data = {
                        'name': name,
                        'confirm_url': f'{os.getenv("DOMAIN")}{url_for("confirm_account")}?id={user_id}&token={confirm_email_token}'
                    }
                    
                    MailService().send(
                        to_email=email,
                        template_id='d-db51f82946674203bf8430c983f4c9e6',
                        dynamic_template_data=dynamic_template_data
                    )
                    
                    return {'msg': 'Check your inbox for a confirmation email'}, 201
        except Exception as e:
            print(e)
        return {'msg': 'server error'}, 500
    
    
    def confirm(self, id, token):
        try:
            engine = current_app.config['engine']
            user_table = current_app.config['tables']['user']
            with Session(engine) as s:
                user = user_table.read(s, id)
                if user and not user.confirmed_email and user.confirm_email_token == token:
                    user_table.update(s, id, {
                        'confirmed_email': True,
                        'confirm_email_token': ''
                    })
                    session['logged_in'] = True
                    session['id'] = user.id
                    session['email'] = user.email
                    session['name'] = user.name
                    session['user_role_id'] = user.user_role_id
        except Exception as e:
            print(e)
        return redirect(url_for('index'))


    def logout(self):
        session.clear()
        return redirect(url_for('index'))
    
    
    def send_password_reset(self, email):
        try:
            engine = current_app.config['engine']
            user_table = current_app.config['tables']['user']
            with Session(engine) as s:
                user = user_table.find(s, email)
                if user:
                    reset_password_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    user_table.update(s, user.id, {
                        'reset_password_token': reset_password_token
                    })
                    dynamic_template_data = {
                        'password_reset_url': f'{os.getenv("DOMAIN")}{url_for("reset_password")}?id={user.id}&token={reset_password_token}'
                    }
                    MailService().send(
                        to_email=email,
                        template_id='d-99786b505b7b4c249bd45efde7c61000',
                        dynamic_template_data=dynamic_template_data
                    )
                    return {'msg': 'Check your inbox for password reset instructions'}, 200
                else:
                    return {'msg': 'This email is not registered'}, 404
        except Exception as e:
            print(e)
        return {'msg': 'server error'}, 500

    def reset_password(self, password):
        return {'msg': 'success'}, 200