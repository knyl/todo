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
        data = json.dumps({'title':title})
        rv1 = self.app.post('/todos', data = data,
                            content_type='application/json')
        assert '201 CREATED' in rv1.status
        assert 'id' in rv1.data
        rv = self.app.get('/todos/1')
        assert title in rv.data

    def test_get_todo_not_found(self):
        rv = self.app.get('/todos/4')
        assert '404 NOT FOUND' in rv.status

if __name__ == '__main__':
    unittest.main()
