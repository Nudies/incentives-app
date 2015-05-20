from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField, DateField, FloatField
from wtforms.validators import Required, EqualTo, Email

class LoginForm(Form):
  email = TextField('Email address', [Required(), Email()])
  password = PasswordField('Password', [Required()])
  
class RegisterForm(Form):
  name = TextField('Name', [Required()])
  email = TextField('Email address', [Required(), Email()])
  password = PasswordField('Password', [Required()])
  confirm = PasswordField('Repeat Password', [
      Required(),
      EqualTo('password', message='Passwords must match')
      ])
  recaptcha = RecaptchaField()
  
class IncentiveForm(Form):
  date = DateField('Date:', [Required()], format='%m/%d/%Y')
  payable_to = TextField('Payable To:', [Required()])
  client = TextField('Client:', [Required()])
  opp_name = TextField('Opp Name:', [Required()])
  dec_project = TextField('Decipher Project #:', [Required()])
  po_num = TextField('PO#:', [Required()])
  amount = FloatField('Amount:', [Required()])
  requested_by = TextField('Requested By:', [Required()])