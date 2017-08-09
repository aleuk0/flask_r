import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):    # создает клиента тестирования и базу данных
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        #flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self): # для удаления базы данных по окончанию теста
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):    # тест доступа к корню и наличия записей
        rv = self.app.get('/')
        #метод assert ожидает последовательность байтов, а не строку.
        #Чтобы преобразовать строку в последовательность байтов, можно
        #воспользоваться методом str.encode()
        assert "Unbelievable. No entries here so far".encode() in rv.data

    def login(self, username, password):    #тест входа
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):   #тест выхода
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):    #тест успешного входа и выхода
        rv = self.login('admin', 'default')
        assert 'You were logged in'.encode() in rv.data
        rv = self.logout()
        assert 'You were logged out'.encode() in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username'.encode() in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password'.encode() in rv.data

    def test_messages(self):   # Тестирование добавления сообщений
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far'.encode() not in rv.data
        assert '&lt;Hello&gt;'.encode() in rv.data
        assert '<strong>HTML</strong> allowed here'.encode() in rv.data

if __name__ == '__main__':
    unittest.main()
