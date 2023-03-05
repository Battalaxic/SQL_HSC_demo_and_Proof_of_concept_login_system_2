from flask import Flask, render_template, request, session, redirect, url_for
import data_demo
import os
from functools import wraps
import password_encryption as pwd_e
import password_registration as pdr

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]

def login_required(f):
    '''Edited from https://flask.palletsprojects.com/en/2.2.x/patterns/viewdecorators/'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# def username_validate(username):
#     with conn.cursor() as cur:
#         cur.execute("SELECT * FROM users WHERE username LIKE %s", (username,))
#         if cur.fetchone():
#             if len(cur.fetchone()) > 0:
#                 username_iteration = len(cur.fetchone())
#                 username = f"{username}{username_iteration}"
#     return username

@app.route('/')
@login_required
def home():  # put application's code here
    return 'Hello World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with conn.cursor() as cur:
            cur.execute("SELECT password FROM users WHERE username = %s", (username,))
            correct_password_hash = cur.fetchone()[0]
            print(correct_password_hash)
            if pwd_e.check_password(password, correct_password_hash):
                user = username
            #cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            #user = cur.fetchone()
            print(user)

        if user:
            session['user_id'] = user
            return redirect('/')
        else:
            return render_template("login.html", error="Invalid username or password")
            #see flask flash
            #see bcrypt for salting and hashing

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        #TODO: Do this in javascript, but show if a username has
        #      already been taken after a specified time delay when user stops inputting
        #username = username_validate(username)
        password = request.form['password']
        hashed_password = pwd_e.encrypt_password(password)
        if not pdr.is_secure_password(password)[0]:
            print(pdr.is_secure_password(password))
            return render_template("register.html", password_features=pdr.subroutine(password))
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
            user = cur.fetchone()
            print('in register, user is:',user)


        if user:
            session['user_id'] = user[0]
            return redirect('/')
        else:
            print('register')
            return render_template("register.html", error="Invalid username or password")
            #TODO: password security requirement
            #see flask flash
            #see bcrypt for salting and hashing

    return render_template('register.html')

@app.route('/logout')
def logout():
    # Check if the user is logged in
    session.clear()
    return redirect('/login')

@app.route('/protected')
def protected():
    # Check if the user is logged in
    print(session)
    if 'user_id' in session:
        return 'Secret protected page'
    else:
        return redirect(url_for('login'))
    # Investigate decorators

conn = data_demo.connect_to_db()

if __name__ == '__main__':
    app.run()
