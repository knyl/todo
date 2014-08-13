class SimpleDb:

    def __init__(self):
        self.todo_list = [{'id':1, 'title':'todo item 1'},
                          {'id':2, 'title':'todo item 2'}
                         ]

    def get_list(self):
        return self.todo_list

    def get_todo(self, todo_id):
        for todo in self.todo_list:
            if todo['id'] == todo_id:
              return todo
        return None

    def add_todo(self, title):
        self.todo_list.append({'title':title})
