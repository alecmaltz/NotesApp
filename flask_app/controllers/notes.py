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

"""starting page"""
@app.route('/')
def index():
    return render_template("login_reg.html")


"""notes page"""
@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect("/")  
    else:
        data = {
            'id' : session['user_id']
        }
        return render_template("note_dashboard.html" , user = User.get_one(data) , all_notes = note.get_all_with_users())


"""add note"""
@app.route('/create_note')
def create_note():
    if "user_id" not in session:
        return redirect("/")  
    else:
        data = {
            'id' : session['user_id']
        }
        return render_template("note_create.html", user = User.get_one(data))


"""note to db"""
@app.route('/process/note', methods=['POST'])
def send_note():
    data = {
        "user_id" : session['user_id'],
        "title" : request.form['title'],
        "note_date" : request.form['note_date'],
        "description" : request.form['description'],
    }
    note.save_note(data)
    return redirect('/dashboard')


"""note details"""
@app.route('/note_details/<int:note_id>')
def note_details(note_id):
    if "user_id" not in session:
        return redirect("/")
    else: 
        data = {
            'id' : session['user_id']
        }
        
        return render_template("note_view.html", user=User.get_one(data), notes = note.get_one_with_name(note_id) )


"""delete note"""
@app.route('/notes/delete/<int:note_id>')
def delete(note_id):
    data = {
        "id" : note_id
    } 
    note.destroy(data)
    return redirect('/dashboard')


"""edit note"""
@app.route('/notes/edit/<int:note_id>')
def edit_note(note_id):
    if "user_id" not in session:
        return redirect("/")
    else: 
        data = {
            'id' : session['user_id']
        }
        return render_template('Note_edit.html', user=User.get_one(data), notes = note.get_one_with_name(note_id))

"""update note"""
@app.route('/update/<int:note_id>', methods=['POST'])
def note_update(note_id):
    data = {
        "note_id " : note_id,
        "user_id" : session['user_id'],
        "title" : request.form['title'],
        "date" : request.form['date'],
        "desc" : request.form['desc'],
    }
    note.update(data)
    return redirect('/dashboard')
