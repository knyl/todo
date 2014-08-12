class SimpleDb:

    def __init__(self):
        self.todo_list = [{'title':'todo item 1'},
                          {'title':'todo item 2'}
                         ]

    def get_list(self):
        return self.todo_list

    def add_todo(self, title):
        self.todo_list.append({'title':title})
