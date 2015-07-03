from re import search

from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, DateField, SelectField, RadioField
from wtforms.validators import Required, EqualTo, Email, Length, ValidationError


# Custom validation
def add_dollar(form, field):
    if field.data[0] != '$':
        field.data = '$' + field.data


def character_check(form, field):
    if search(r'[^0-9$,.]', field.data):
        raise ValidationError('This field can only contain 0-9 $ , . charaters.')


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
    amount = TextField('Amount:', [Required(), character_check, add_dollar])
    requested_by = TextField('Requested By:', [Required()])


class EditUserForm(Form):
    user = SelectField('User', [Required()], coerce=int)
    new_name = TextField('Name')
    new_email = TextField('Email address')
    new_password = PasswordField('Password')
    new_role = SelectField('Role', coerce=int, choices=[(3, 'None'), (2, 'user'),
                           (1, 'staff'), (0, 'admin')])


class ApproveForm(Form):
    incentive = SelectField('Incentive', [Required()], coerce=int)
    approved = RadioField('Approved', [Required()], coerce=int,
                          choices=[(2, 'Approve')])
