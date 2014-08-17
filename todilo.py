import os
from flask import Flask, json, abort, request, render_template, make_response
import simple_db

app = Flask(__name__)
app.config.from_object(__name__)
db = simple_db.SimpleDb()

# TODO: Put all these in a config file
app.config.update(dict(
    SECRET_KEY = 'dev_key',
    USERNAME = 'admin',
    PASSWORD = 'admin',
    DEBUG = True
    ))

app.config.from_envvar('TODILO_SETTINGS', silent=True)

@app.route('/')
def hello():
    return render_template("list_todos.html")

@app.route('/todos', methods=['GET'])
def list_todos():
    app.logger.info("Listing todos")
    todos = db.get_list()
    return json.dumps(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    app.logger.info('Getting POST request with data: %s', request.data)
    todo = request.get_json()
    app.logger.info('Adding todo with title: %s', todo[u'title'])
    todo_id = db.add_todo(todo)
    return json.dumps({u'id':todo_id}), 201

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    app.logger.info('Fetching todo with id: %s', todo_id)
    todo = db.get_todo(todo_id)
    if todo == None:
        abort(404)
    return json.dumps(todo)

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    app.logger.info('Updating todo with id: %s', todo_id)
    todo = db.get_todo(todo_id)
    app.logger.info('Tried to fetch todo: %s', todo)
    if todo == None:
        abort(404)
    updated_todo = db.update_todo(request.get_json())
    return json.dumps(updated_todo)

@app.route('/todos/order', methods=['PUT'])
def update_order():
    ids = request.get_json()
    app.logger.info('Updating ordering to: %s', ids)
    db.update_order(ids[u'ids'])
    return ''

@app.errorhandler(404)
def not_found(error):
    return make_response(json.dumps( { 'error': 'Not found' } ), 404)

if __name__ == '__main__':
    app.run()
