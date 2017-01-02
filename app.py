from flask import Flask, render_template, g, request, session, redirect, url_for, escape, abort
from flask_socketio import SocketIO, emit, join_room
from flask_login import LoginManager, login_user, logout_user, current_user

import os
import sqlite3

#from game import Game

app = Flask(__name__)

#App Config
app.config.from_object(__name__)
#app.config.update(dict(
#    DATABASE=os.path.join(app.root_path, 'airts.db'),
#    SECRET_KEY = "420 lmao"
#))
app.config.from_envvar('AIRTS_SETTINGS', silent=True)


socketio = SocketIO(app)

#loginManager = LoginManager()
#loginManager.init_app(app)


## Database fuctions ##
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initialises the database from [flask initdb] command"""
    init_db()
    print "INFO: Initialised the database."

def connect_db():
    """Connects to the specified database"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if none is yet for the current app context"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


## Routing Functions ##
@app.route("/")
def index():
    user = None
    if 'username' in session:
        user = escape(session['username'])
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            error = "Invalid username or password"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/game', methods=['GET'])
def gamepage():
    if not session.get('logged_in'):
        abort(401)
    
    if request.args.get('spawn'):
        x, y, z = request.args['spawn'].split(',')
        d = {'x': x, 'y': y, 'texture': url_for('static', filename='images/'+z+'.png')}
        print d
        emit('spawn', d, namespace='/game', room="room")
    
    return render_template('game.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    uError = None
    pError = None
    if request.method == 'POST':
        if not reg_unique_name(request.form['username']):
            uError = "Name already taken"
        elif not reg_good_pass(request.form['password']):
            pError = "Password not good"
        elif request.form['password'] != request.form['confirmpass']:
            pError = "Passwords don't match"
        else:
            register_user(request.form['username'], request.form['password'])
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('register.html', uError=uError, pError=pError) 

## SocketIO Function ##
@socketio.on('join')
def on_join(data):
    join_room("room")
    emit('join', {'game_id': "room"})



## Helper Functions ##
def valid_login(name, pword):
    db = get_db()
    cur = db.execute('select * from users where name == ? and password == ?',
            [name, pword]) 
    return len(cur.fetchall()) == 1

def reg_unique_name(name):
    db = get_db()
    cur = db.execute('select name from users where name == ?', [name])
    return len(cur.fetchall()) == 0

def reg_good_pass(passw):
    return True

def register_user(name, passw):
    db = get_db()
    db.execute('insert into users (name, password) values (?, ?)',
            [name, passw])
    db.commit()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
