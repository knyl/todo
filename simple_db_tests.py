import simple_db
import unittest

class SimpleDbTests(unittest.TestCase):

    def setUp(self):
        self.db = simple_db.SimpleDb()

    def tearDown(self):
        self.db.todos = []
        pass

    def test_empty_db(self):
        assert [] == self.db.get_list()

    def test_add_and_get_one_todo(self):
        title = 'todo item 1'
        self.db.add_todo({u'title':title, u'done':False})
        todo = self.db.get_todo(1)
        assert {'title':title, 'done':False, 'id':1} == todo

    def test_update_todo(self):
        todo = {'title':'todo1', 'done':False}
        todo_id = self.db.add_todo(todo)
        todo[u'id'] = todo_id
        assert todo == self.db.get_todo(todo_id)
        todo[u'done'] = True
        self.db.update_todo(todo)
        assert todo == self.db.get_todo(todo_id)

    def test_update_order(self):
        todo1 = {u'title':'todo1', u'prio':0}
        todo2 = {u'title':'todo2', u'prio':1}
        id1 = self.db.add_todo(todo1)
        id2 = self.db.add_todo(todo2)
        self.db.update_order([id2, id1])
        todo1 = self.db.get_todo(id1)
        assert 1 == todo1[u'prio']
        todo2 = self.db.get_todo(id2)
        assert 0 == todo2[u'prio']


if __name__ == '__main__':
    unittest.main()
