from app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt

from app.models.user import User

bcrypt = Bcrypt(app)


@app.route('/main')
def index():
    return render_template('login.html')


# register user
@app.route('/register', methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)
    flash('You registered yourself successfully!')

    if not is_valid:
        return redirect("/main")
    print(is_valid)
    new_user = {
        'full_name': request.form['fullname'],
        'email': request.form['email'],
        'password': request.form['password'],
        'password': bcrypt.generate_password_hash(request.form['password']),
    }

    id = User.save(new_user)
    if not id:
        flash("Email already taken.", "register")
        return redirect('/main')
    session['user_id'] = id
    return redirect('/dashboard')

# validate email


@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.get_email(data)
    if not user:
        flash('Invalid email or password', 'login')
        return redirect('/main')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password', 'login')
        return redirect('/main')

    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/main')
