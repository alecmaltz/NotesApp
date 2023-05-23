from flask import render_template,redirect,request,session, flash
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.note import note



"""register user"""
@app.route('/register', methods=['POST'])
def create():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name":request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash,
        "confirm_password" : request.form['confirm_password']
    }
    if not User.validate_user(request.form):
        return redirect('/')
    
    if not request.form['password'] == request.form['confirm_password'] :
        flash("Password doesnt match")
        return redirect('/')

    if not User.validate_registration(request.form):
        return redirect('/')

    else :
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect('/dashboard')


"""log-in user"""
@app.route('/login', methods=['POST' , 'GET'])
def login():
    data= {
        "email": request.form['email']
    }
    user_in_db = User.login(data)
    if not user_in_db:
        flash("Invalid Email")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password")
        return redirect("/")
    
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


"""log user out"""
@app.route('/logout')
def logout():
    session.pop("user_id" , 0)

    return redirect("/")
