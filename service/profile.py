from flask import current_app, session, render_template, redirect

class ProfileService:
    def read(self):
        if 'logged_in' in session and session['logged_in']:
            return render_template("profile.html")
        return redirect(url_for('index'))
    
    def update(self, request):
        if not 'logged_in' in session or not session['logged_in']:
            return {'msg': 'Please log in to change your information'}, 401
        try:
            user_table = current_app.config['tables']['user']
            if 'password' in request.json['fields']:
                user = user_table.find(session['email'], request.json['password'])
                if not user:
                    return {'msg': 'Incorrect password'}, 401
            user_table.update(session['id'], request.json['fields'])
            user = user_table.read(session['id'])
            session['name'] = user.name
            session['email'] = user.email
            return {'msg': 'Success'}, 200
        except Exception as e:
            print(e)
        return {'msg': 'Server Error'}, 500