from flask import current_app, session, render_template, redirect
from database.mysql_implementation.user import *

class ProfileService:
    def read(self):
        if 'logged_in' in session and session['logged_in']:
            return render_template("profile.html")
        return redirect(url_for('index'))
    
    def update(self, fields, password=None):
        if not 'logged_in' in session or not session['logged_in']:
            return {'msg': 'Please log in to change your information'}, 401
        try:
            engine = current_app.config['engine']
            user_table = current_app.config['tables']['user']
            with Session(engine) as s:
                if 'password' in fields:
                    user = user_table.find(s, session['email'], password)
                    if not user:
                        return {'msg': 'Incorrect password'}, 401
                user_table.update(s, session['id'], fields)
                user = user_table.read(s, session['id'])
                session['name'] = user.name
                session['email'] = user.email
            return {'msg': 'Success'}, 200
        except Exception as e:
            print(e)
        return {'msg': 'Server Error'}, 500