import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from LoginForm import LoginForm, MessageForm

#create application
app = Flask(__name__)
app.config.from_object(__name__)

#add configuration
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'chatr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            return redirect(url_for('/'))
        elif request.form['password'] != app.config['PASSWORD']:
            return redirect(url_for('/'))
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('chat'))
    return render_template('login.html', error=error, form=form)


@app.route('/', methods=['GET'])
def index():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/chat', methods=['GET'])
def chat():
    db = get_db()
    cursor = db.execute('select * from messages order by Timestamp DESC')
    messages = cursor.fetchall()

    form = MessageForm()

    return render_template('chat.html', messages=messages, form=form)


@app.route('/add_message', methods=['POST'])
def add_message():
    db = get_db()
    db.execute('INSERT INTO messages (sender, receiver, text) VALUES (0, 1, ?)', [request.form['body']])
    db.commit()
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run()