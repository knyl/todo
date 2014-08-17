import os
from flask import Flask, jsonify, abort, request, render_template, make_response
import simple_db
import logging

app = Flask(__name__)
app.config.from_object(__name__)
db = simple_db.SimpleDb()
logging.basicConfig(filename='todilo.log',level=logging.DEBUG)

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
    logging.info("Listing todos")
    todos = db.get_list()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    logging.info('Getting POST request with data: %s', request.data)
    todo = request.get_json()
    logging.info('Adding todo with title: %s', todo[u'title'])
    todo_id = db.add_todo(todo)
    return jsonify({u'id':todo_id}), 201

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    logging.info('Fetching todo with id: %s', todo_id)
    todo = db.get_todo(todo_id)
    if todo == None:
        abort(404)
    return jsonify(todo)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

if __name__ == '__main__':
    app.run()
