from flask import Flask, render_template, request, session, redirect, url_for
import data_demo
import os
from functools import wraps

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
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cur.fetchone()
            print(user)

        if user:
            session['user_id'] = user[0]
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
        print(username)
        password = request.form['password']
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
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
