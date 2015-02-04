import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        #flaskr.add.config['TESTING'] = True # disables error catching so that
                                            # you can get better error reports
                                            # when performing tests against the
                                            # application in question
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    # the keyword 'test' in the function allows unittest to
    # automatically identify the method as a test to run
    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data = dict(
            username = username,
            password = password
        ), follow_redirects = True)

    def logout(self):
        return self.app.get('/logout', follow_redirects = True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data

        rv = self.logout()
        assert 'You were logged out' in rv.data

        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data

        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data = dict(
            title = '<Hello>',
            text = '<strong>HTML</strong> allowed here'
        ), follow_redirects = True)

        # check that HTML is allowed in the text but not
        # in the title itself, as intended in the app
        
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data
        
if __name__ == '__main__':
    unittest.main()