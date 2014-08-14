import simple_db
import unittest

class SimpleDbTests(unittest.TestCase):

    def setUp(self):
        self.db = simple_db.SimpleDb()

    def tearDown(self):
        pass

    def test_empty_db(self):
        assert [] == self.db.get_list_with_order()

    def test_add_and_get_one_todo(self):
        title = 'todo item 1'
        self.db.add_todo(title)
        todo = self.db.get_todo(1)
        assert {'title':title, 'done':False, 'id':1} == todo

    def test_list_with_order(self):
        self.db.todos = []
        title1 = 'todo item 1'
        title2 = 'todo item 2'
        self.db.add_todo(title1)
        self.db.add_todo(title2)
        todos = self.db.get_list_with_order()
        [todo1, todo2] = todos
        assert todo1['id'] == 2 and todo1['priority'] == 1
        assert todo2['id'] == 1 and todo2['priority'] == 2


if __name__ == '__main__':
    unittest.main()
