import todilo
import unittest

class TodiloTestCase(unittest.TestCase):

    def setUp(self):
        todilo.app.config['TESTING'] = True
        self.app = todilo.app.test_client()

    def tearDown(self):
        pass

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Hello world!' in rv.data

    def test_get_todo(self):
        rv = self.app.get('/todo/1')
        assert 'todo item 1' in rv.data

    def test_get_todo_not_found(self):
        rv = self.app.get('/todo/4')
        assert '404 NOT FOUND' in rv.status

if __name__ == '__main__':
    unittest.main()
