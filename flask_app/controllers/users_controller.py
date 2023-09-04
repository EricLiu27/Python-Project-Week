from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User


from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument

from flask_app.models.forum_model import Forum

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/users/dashboard')
    return render_template('index.html')



@app.route('/users/create')
def create():
    if 'user_id' in session:
        return redirect('/users/dashboard')
    return render_template('users_create.html')



@app.route('/users/register', methods=['POST'])
def register():
    if not User.is_valid(request.form):
        return redirect('/users/create')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password' : hashed_pass,
        'cpass': hashed_pass
    }
    logged_user_id = User.create(data)
    session['user_id'] = logged_user_id
    return redirect('/users/dashboard')

@app.route('/users/login', methods = ['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    potential_user = User.get_by_email(data)
    if not potential_user:
        flash('Invalid credentials','log')
        return redirect('/users/create')
    if not bcrypt.check_password_hash(potential_user.password, request.form['password']):
        flash('Invalid credentials','log')
        return redirect('/')
    session ['user_id'] = potential_user.id
    return redirect('/users/dashboard')


@app.route('/users/streamers')
def streamers():
    data = {
        'id' : session ['user_id']
    }
    logged_user = User.get_by_id(data)
    return render_template('users_streamers.html', logged_user = logged_user)



@app.route('/users/videos')
def videos ():
    data = {
        'id' : session ['user_id']
    }
    logged_user = User.get_by_id(data)
    return render_template('users_videos.html', logged_user = logged_user)


@app.route('/users/dashboard')
def dashboard():
    if 'user_id' not in session: 
        return redirect ('/')
    data = {
        'id' : session ['user_id']
    }
    logged_user = User.get_by_id(data)
    return render_template ('users_dashboard.html',logged_user=logged_user)

@app.route('/users/logout')
def logout():
    del session['user_id']
    return redirect ('/')
    
    





