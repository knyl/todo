import os
from flask import Flask, json, abort, request, render_template, make_response, g
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

# TODO: Put all these in a config file
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'todilo.db'),
    SECRET_KEY = 'dev_key',
    USERNAME = 'admin',
    PASSWORD = 'default',
    DEBUG = True
    ))

app.config.from_envvar('TODILO_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'],
                         detect_types=sqlite3.PARSE_DECLTYPES)
    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("boolean", lambda v: bool(int(v)))
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def hello():
    return render_template("list_todos.html")

@app.route('/todos', methods=['GET'])
def list_todos():
    app.logger.info("Listing todos")
    db = get_db()
    cur = db.execute('select id, title, done, prio from todolist')
    todos = []
    for (todo_id, title, done, prio) in cur.fetchall():
        todos.append({'id':todo_id, 'title':title, 'done':done, 'prio':prio})
    return json.dumps(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    app.logger.info('Getting POST request with data: %s', request.data)
    todo = request.get_json()
    app.logger.info('Adding todo with title: %s', todo[u'title'])
    db = get_db()
    cur = db.execute('insert into todolist (title, prio, done) values (?, ?, ?)',
                   [todo[u'title'], todo[u'prio'], todo[u'done']])
    todo_id = cur.lastrowid
    db.commit()
    return json.dumps({u'id':todo_id}), 201

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    app.logger.info('Fetching todo with id: %s', todo_id)
    db = get_db()
    todo = get_todo(db, todo_id)
    if todo == None:
        abort(404)
    app.logger.info("todo is: %s", todo)
    return json.dumps(todo)

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    app.logger.info('Updating todo with id: %s', todo_id)
    db = get_db()
    if get_todo(db, todo_id) == None:
        abort(404)
    todo = request.get_json()
    app.logger.info('new values: %s', todo)
    cur = db.execute('update todolist set title=(?), done=(?) where id=(?)',
                     [todo[u'title'], todo[u'done'], todo[u'id']])
    db.commit()
    return ''

@app.route('/todos/order', methods=['PUT'])
def update_order():
    ids = request.get_json()
    app.logger.info('Updating ordering to: %s', ids)
    db = get_db()
    prio = 0
    for todo_id in ids['ids']:
        db.execute('update todolist set prio=(?) where id=(?)',
                   [prio, todo_id])
        db.commit()
        prio += 1
    return ''

@app.errorhandler(404)
def not_found(error):
    return make_response(json.dumps({'error': 'Not found'}), 404)

def get_todo(db, todo_id):
    cur = db.execute('select id, title, done, prio from todolist where id=(?)',
                     [todo_id])
    result = cur.fetchall()
    if result == []:
        return None
    else:
        [(todo_id, title, done, prio)] = result
        return {'id':todo_id, 'title':title, 'done':done, 'prio':prio}

if __name__ == '__main__':
    app.run()
