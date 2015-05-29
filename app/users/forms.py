from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField, DateField, FloatField, SelectField
from wtforms.validators import Required, EqualTo, Email, Length

class LoginForm(Form):
  email = TextField('Email address', [Required(), Email()])
  password = PasswordField('Password', [Required()])
  
class RegisterForm(Form):
  name = TextField('Name', [Required()])
  email = TextField('Email address', [Required(), Email()])
  password = PasswordField('Password', [Required(), Length(min=6)])
  confirm = PasswordField('Repeat Password', [
      Required(),
      EqualTo('password', message='Passwords must match')
      ])
  recaptcha = RecaptchaField()
  
class ResetForm(Form):
  email = TextField('Email address', [Required(), Email()])
  recaptcha = RecaptchaField()
  
class NewPasswordForm(Form):
  new_password = PasswordField('New Password', [Required(), Length(min=6)])
  new_confirm = PasswordField('Repeat Password', [
      Required(),
      EqualTo('new_password', message='Passwords must match')
      ])
  
class IncentiveForm(Form):
  date = DateField('Date:', [Required()], format='%m/%d/%Y')
  payable_to = TextField('Payable To:', [Required()])
  client = TextField('Client:', [Required()])
  opp_name = TextField('Opp Name:', [Required()])
  dec_project = TextField('Decipher Project #:', [Required()])
  po_num = TextField('PO#:', [Required()])
  amount = FloatField('Amount:', [Required()])
  requested_by = TextField('Requested By:', [Required()])
  

class EditUserForm(Form):
  user = SelectField('User', [Required()], coerce=int)
  new_name = TextField('Name')
  new_email = TextField('Email address')
  new_role = SelectField('Role', coerce=int, choices=[(3, 'None'),(2, 'user'), (1, 'staff'), (0, 'admin')])
  