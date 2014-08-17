class SimpleDb:

    def __init__(self):
        self.todos = []

    def get_list(self):
        return self.todos

    def get_todo(self, todo_id):
        for todo in self.todos:
            if todo[u'id'] == todo_id:
              return todo
        return None

    def add_todo(self, todo):
        next_id = get_next_id(self.todos)
        todo[u'id'] = next_id
        self.todos.append(todo)
        return next_id

def get_next_id(todos):
  ids = [todo[u'id'] for todo in todos]
  if ids == []:
    return 1
  else:
    return max(ids)+1
