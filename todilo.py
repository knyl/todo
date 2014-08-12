import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash
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
def list_todos():
    #username = request.args.get('UserName')
    #password = request.args.get('Password')
    todos = db.get_list()
    return render_template('list_todos.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    if not session.get('logged_in'):
        abort(401)
    #db = get_db()
    #db.execute('insert into entries (title, text) values (?, ?)',
    #           [request.form['title'], request.form['text']])
    #db.commit()
    title = request.form['title']
    db.add_todo(title)
    flash('New todo was successfully added')
    return redirect(url_for('list_todos'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
              error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('list_todos'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('list_todos'))

if __name__ == '__main__':
    app.run()
