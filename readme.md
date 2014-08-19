# Todilo

A small todo-application written in Python/Flask and Javascript/Backbone.js

Lets you add todos, edit them and reorder them.

### Backend API
All data posted to, or retrieved from the API must be valid JSON.

#### Todo object
* id - unique identifier
* title - title of the todo
* prio - priority of the todo
* done - whether the todo is done or not

#### Resources
* GET /todos
List the current todos.
  * **Response** A collection with Todo objects.

* GET /todos/<todo_id>
Retrieve a specific todo.
  * **Response** The requested Todo object, or 404 Not Found, if it doesn't exist.

* POST /todos
Add a new todo.
  * **Input** A Todo object.
  * **Response** 201 Created, if the data is valid.

* PUT /todos/<todo_id>
Update a todo.
  * **Input** A Todo object.
  * **Response** 200 OK, if the data is valid, and the object exists.

* PUT /todos/order
Update the order of the todos.
  * **Input** A collection with todo_ids.
  * **Response** 200 OK, if the data is valid, and the todos exists.

### TODO
* Clean up tests and code
* Put in a real database
* Error handling
* Make button submit the todo
* DELETE /todos/<id> to clear a todo
* XSS/SQL injections/bad stuff - clean/escape the todo text?
