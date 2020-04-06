import json

from flask import Flask, g
import sqlite3
from Class import User
DATABASE = 'heroku.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def clse_connection(expection):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/users')
def showUsers():
    query = 'select * from user'
    rs = query_db(query, args=(), one=False)
    users = []
    for row in rs:
        user = User.User(row[0], row[1])
        users.append(user.__dict__)
    return json.dumps(users)


if __name__ == '__main__':
    app.run()
