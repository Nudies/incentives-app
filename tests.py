import os
from app import app, db
from app.users.models import User, Incentive
import unittest
import tempfile

class AppTestCase(unittest.TestCase):
  def setUp(self):
    _basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(_basedir, 'test.db')
    self.app = app.test_client()
    db.create_all()
  
  def tearDown(self):
    db.session.remove()
    db.drop_all()
  
  def test_empty_db(self):
    '''no user logged in should redirect to /login/'''
    request = self.app.get('/')
    assert 'Redirecting' in request.data
  
  def test_register(self):
    request = self.app.post('/register/', data=dict(name='John Doe',
    email='jd@decipherinc.com', password='abc123', confirm='abc123'), follow_redirects=True)
    u = User.query.filter_by(email='jd@decipherinc.com').first()
    assert 'Thanks for registering' in request.data
    assert u.name == 'John Doe'
    assert u.email == 'jd@decipherinc.com'
    assert u.password != 'abc123'
    
if __name__ == '__main__':
  unittest.main()