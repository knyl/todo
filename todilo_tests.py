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

    def xtest_empty_db(self):
        rv = self.app.get('/todos')
        assert '200 OK' in rv.status
        assert '' in rv.data

    def xtest_add_and_get_todo(self):
        title = 'todo item 1'
        data = json.dumps({'title':title})
        rv1 = self.app.post('/todos', data = data,
                            content_type='application/json')
        assert '201 CREATED' in rv1.status
        assert 'id' in rv1.data
        rv = self.app.get('/todos/1')
        assert title in rv.data

    def xtest_get_todo_not_found(self):
        rv = self.app.get('/todos/4')
        assert '404 NOT FOUND' in rv.status

    def test_update_todo(self):
        title = 'todo item 1'
        todo = {'title':title, 'prio': 1, 'done':False}
        data = json.dumps(todo)
        rv1 = self.app.post('/todos', data = data,
                            content_type='application/json')
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

if __name__ == '__main__':
    unittest.main()
