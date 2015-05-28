import os
from app import app, db
from app.users.models import User, Incentive
import unittest
import tempfile

class AppTestCase(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    _basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(_basedir, 'test.db')
    cls.app = app.test_client()
    db.create_all()
  
  @classmethod
  def tearDownClass(cls):
    db.session.remove()
    db.drop_all()
  
  def register(self, name, email, password):
    return self.app.post('/register/', data=dict(name=name,
    email=email, password=password, confirm=password), follow_redirects=True)
    
  def login(self, email, password):
    return self.app.post('/login/', data=dict(email=email, password=password), follow_redirects=True)
  
  def logout(self):
    return self.app.get('/logout/', follow_redirects=True)
  
  def test_empty_db(self):
    request = self.app.get('/', follow_redirects=True)
    assert 'Log in to your account' in request.data
  
  def test_register_logout_login(self):
      #register
      request = self.register('John Doe', 'jd@decipherinc.com', 'abc123')
      u = User.query.filter_by(email='jd@decipherinc.com').first()
      assert 'Thanks for registering' in request.data
      assert u.name == 'John Doe'
      assert u.email == 'jd@decipherinc.com'
      assert u.password != 'abc123'
    
      #logout
      request = self.logout()
      assert 'You were successfully logged out' in request.data
  
      #login
      request = self.login('jd@decipherinc.com', 'abc123')
      assert 'Welcome back, John Doe!' in request.data
    
  def test_email_reset_fail(self):
    request = self.app.post('/reset/', data=dict(email='test@test.com'), follow_redirects=True)
    assert 'The email test@test.com does not exist!' in request.data
    
  def test_reset_pw_bad_link(self):
    request = self.app.post('/reset/id/asdgfdaasd/', data=dict(new_password='abc123', new_confirm='abc123'), follow_redirects=True)
    assert 404 == request.status_code
    assert '404' in request.data
    
    
if __name__ == '__main__':
  unittest.main()