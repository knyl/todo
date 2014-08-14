import os
from flask import Flask, request, abort, json, render_template,\
                  render_template, make_response
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
    todos = db.get_list_with_order()
    return json.dumps(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    title = request.form['title']
    db.add_todo(title)
    return ('', 201, [])

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = db.get_todo(todo_id)
    if todo == None:
        abort(404)
    return json.dumps(todo)

if __name__ == '__main__':
    app.run()
