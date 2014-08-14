class SimpleDb:

    def __init__(self):
        self.todo_list = []

    def get_list(self):
        return self.todo_list

    def get_todo(self, todo_id):
        for todo in self.todo_list:
            if todo['id'] == todo_id:
              return todo
        return None

    def add_todo(self, title):
        next_id = get_next_id(self.todo_list)
        self.todo_list.append({'id':next_id, 'title':title, 'done':False})

def get_next_id(todos):
  ids = [todo['id'] for todo in todos]
  if ids == []:
    return 1
  else:
    return max(ids)+1
