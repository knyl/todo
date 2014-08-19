import todilo
import unittest
from flask import json
import httplib

class TodosEmptyResource(unittest.TestCase):

    def setUp(self):
        todilo.app.config['TESTING'] = True
        self.app = todilo.app.test_client()

    def tearDown(self):
        # TODO: Clear database after tests
        pass

    def test_empty_db(self):
        rv = self.app.get('/todos')
        assert '200 OK' in rv.status
        assert '' in rv.data

    def test_add_and_get_todo(self):
        title = 'todo item 1'
        rv1 = self.post_todo({'title':title})
        assert '201 CREATED' in rv1.status
        assert 'id' in rv1.data
        rv = self.app.get('/todos/1')
        assert title in rv.data

    def test_get_todo_not_found(self):
        rv = self.app.get('/todos/4')
        assert '404 NOT FOUND' in rv.status

    def test_update_todo(self):
        """ Create a todo, then update the done status, and verify that the
            done status is updated.
        """
        title = 'todo item 1'
        todo = {'title':title, 'prio': 1, 'done':False}
        rv1 = self.post_todo(todo)
        assert '201 CREATED' in rv1.status

        data = json.loads(rv1.data)
        todo_id = data[u'id']
        rv2 = self.app.get('/todos/' + str(todo_id))
        original_data = json.loads(rv2.data)
        assert title == original_data[u'title']
        assert False == original_data[u'done']

        todo['id'] = todo_id
        todo['done'] = True
        data2 = json.dumps(todo)
        rv2 = self.app.put('/todos/' + str(todo_id), data = data2,
                           content_type = 'application/json')
        updated_data = json.loads(rv2.data)
        assert '200 OK' in rv2.status
        assert title == updated_data[u'title']
        assert True == updated_data[u'done']

    def test_update_order(self):
        """ Create two todos, update the order of them, and verify that the
            new order is correct.
        """
        todo1 = {'title':'todo1', 'prio': 0, 'done':False}
        rv1 = self.post_todo(todo1)
        todo1_data = json.loads(rv1.data)
        id1 = todo1_data[u'id']

        todo2 = {'title':'todo2', 'prio': 1, 'done':False}
        rv2 = self.post_todo(todo2)
        todo2_data = json.loads(rv2.data)
        id2 = todo2_data[u'id']

        ordering_data = json.dumps({'ids':[id2, id1]})
        rv_ordering = self.app.put('/todos/order', data = ordering_data,
                                   content_type='application/json')
        assert '200 OK' in rv_ordering.status

        updated_todo1_res = self.app.get('/todos/' + str(id1))
        updated_todo1 = json.loads(updated_todo1_res.data)
        assert 1 == updated_todo1[u'prio']

        updated_todo2_res = self.app.get('/todos/' + str(id2))
        updated_todo2 = json.loads(updated_todo2_res.data)
        assert 0 == updated_todo2[u'prio']

    def post_todo(self, todo):
        data = json.dumps(todo)
        result = self.app.post('/todos', data = data,
                               content_type='application/json')
        return result


if __name__ == '__main__':
    unittest.main()
