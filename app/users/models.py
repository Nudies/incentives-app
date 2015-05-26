from app import db
from app.users import constants as USER

class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True)
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(120))
  role = db.Column(db.SmallInteger, default=USER.USER)
  status = db.Column(db.SmallInteger, default=USER.NEW)
  incentives = db.relationship('Incentive', backref='user', lazy='dynamic')
  
  def __init__(self, name=None, email=None, password=None):
    self.name = name
    self.email = email
    self.password = password
    
  def getStatus(self):
    return USER.STATUS[self.status]
    
  def getRole(self):
    return USER.ROLE[self.role]
    
  def __repr__(self):
    return '<User %r>' % (self.name)
    
    
class Incentive(db.Model):
  __tablename__ = 'incentive'
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.String(50))
  payable_to = db.Column(db.String(120))
  client = db.Column(db.String(120))
  opp_name = db.Column(db.String(120))
  dec_project = db.Column(db.String(120))
  po_num = db.Column(db.String(120))
  ammount = db.Column(db.Float)
  requested_by = db.Column(db.String(120))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
  def __init__(self, date=None, payable_to=None, client=None, opp_name=None, dec_project=None, po_num=None, ammount=None, requested_by=None):
    self.date = date
    self.payable_to = payable_to
    self.client = client
    self.opp_name = opp_name
    self.dec_project = dec_project
    self.po_num = po_num
    self.ammount = ammount
    self.requested_by = requested_by
    
  def __repr__(self):
    return '<Incentive %r>' % (self.id)