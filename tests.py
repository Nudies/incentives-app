# This is gross and poorly writen unit tests. 
# I will be rewritting this after I finish the FT
import os
from app import app, db
from app.users.models import User, Incentive
import unittest

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

  def new_incentive(self, date, payable_to, client, opp_name, dec_project, po_num, amount, requested_by):
    return self.app.post('/new-incentive/', data=dict(date=date, payable_to=payable_to, client=client, opp_name=opp_name, dec_project=dec_project, po_num=po_num, amount=amount, requested_by=requested_by), follow_redirects=True)

  def test_a_empty_db(self):
    request = self.app.get('/', follow_redirects=True)
    assert 'Log in to your account' in request.data

  def test_b_register(self):
      request = self.register('John Doe', 'jd@decipherinc.com', 'abc123')
      u = User.query.filter_by(email='jd@decipherinc.com').first()
      assert 'Thanks for registering' in request.data
      assert u.name == 'John Doe'
      assert u.email == 'jd@decipherinc.com'
      assert u.password != 'abc123'

  def test_c_logout(self):
      request = self.logout()
      assert 'You were successfully logged out' in request.data

  def test_d_login(self):
      request = self.login('jd@decipherinc.com', 'abc123')
      assert 'Welcome back, John Doe!' in request.data

  def test_e_email_reset_fail(self):
    request = self.app.post('/reset/', data=dict(email='test@test.com'), follow_redirects=True)
    assert 'The email test@test.com does not exist!' in request.data

  def test_f_reset_pw_bad_link(self):
    request = self.app.post('/reset/id/asdgfdaasd/', data=dict(new_password='abc123', new_confirm='abc123'), follow_redirects=True)
    assert 404 == request.status_code
    assert '404' in request.data

  def test_g_new_incentive(self):
    request = self.new_incentive('05/28/2015', 'test', 'test_client', 'test', 'test123', '123456', 203.45, 'Tester')
    incentive = Incentive.query.filter_by(requested_by='Tester').first()
    assert 'Incentive request submitted for project test123!' in request.data
    assert incentive.date == '2015-05-28'

  def test_h_past_incentive(self):
    request = self.app.get('/past-incentive/')
    assert 'Requests for John Doe' in request.data


if __name__ == '__main__':
  unittest.main()
