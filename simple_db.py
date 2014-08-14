class SimpleDb:

    def __init__(self):
        self.todos = []

    def get_list_with_order(self):
        todos_with_order = []
        prio_nr = 1
        for todo in self.todos:
            todos_with_order.append({'id':todo['id'], 'priority':prio_nr})
            prio_nr = prio_nr + 1
        return todos_with_order

    def get_list(self):
        return self.todos

    def get_todo(self, todo_id):
        for todo in self.todos:
            if todo['id'] == todo_id:
              return todo
        return None

    def add_todo(self, title):
        next_id = get_next_id(self.todos)
        self.todos.insert(0, {'id':next_id, 'title':title, 'done':False})

def get_next_id(todos):
  ids = [todo['id'] for todo in todos]
  if ids == []:
    return 1
  else:
    return max(ids)+1
