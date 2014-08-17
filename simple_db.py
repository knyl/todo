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

    def update_todo(self, updated_todo):
        todo_id = updated_todo[u'id']
        todo = self.get_todo(todo_id)
        self.todos.remove(todo)
        self.todos.append(updated_todo)
        return updated_todo

    def update_order(self, ids):
        order = 0
        new_todo_list = []
        for id in ids:
            todo = self.get_todo(id)
            todo[u'prio'] = order
            new_todo_list.append(todo)
            order = order + 1
        new_todo_list.reverse()
        self.todos = new_todo_list

def get_next_id(todos):
  ids = [todo[u'id'] for todo in todos]
  if ids == []:
    return 1
  else:
    return max(ids)+1
