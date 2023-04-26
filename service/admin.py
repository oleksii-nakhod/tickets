from flask import current_app, session, redirect, render_template

class AdminService:
    def read_users(self):
        if not 'logged_in' in session or not session['logged_in'] or not session['user_role_id'] == 1:
            return redirect(url_for('index'))
        user_table = current_app.config['tables']['user']
        users = user_table.read_all()
        data = {'users': [{
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'user_role_id': user.user_role_id
        } for user in users]}
        return render_template("admin.html", data=data)