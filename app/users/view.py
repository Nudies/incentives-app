from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from flask_mail import Message
from app import db, mail
from app.users.mail import msgr, reset_msg
from app.users.forms import RegisterForm, LoginForm, IncentiveForm, ResetForm, NewPasswordForm
from app.users.models import User, Incentive, PasswordReset
from app.users.decorators import requires_login, get_incentives
from sqlalchemy.exc import IntegrityError

mod = Blueprint('users', __name__)

@mod.route('/')
@requires_login
def home():
  return render_template('users/profile.html', user=g.user)


@mod.before_request
def before_request():
  """
  Get user's profile from db before request is handled.
  """
  g.user = None
  g.incentives = None
  if 'user_id' in session:
    g.user = User.query.get(session['user_id'])


@mod.route('/login/', methods=['GET', 'POST'])
def login():
  """
  Login Form
  """
  form = LoginForm(request.form)
  
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and check_password_hash(user.password, form.password.data):
      session['user_id'] = user.id
      flash('Welcome back, %s!' % user.name, category='success')
      return redirect(url_for('users.home'))
    flash('Email or password is wrong', category='error-message')
  return render_template('users/login.html', form=form)
 
 
@mod.route('/logout/')
def logout():
  """
  Drops user session
  """
  session.pop('user_id', None)
  flash('You were successfully logged out!', category='success')
  return redirect(url_for('users.home'))
  
  
@mod.route('/register/', methods=['GET', 'POST'])
def register():
  """
  Registration Form
  """
  form = RegisterForm(request.form)
  if form.validate_on_submit():
    #create new user instance not yet stored in db
    user = User(name=form.name.data, email=form.email.data, password=generate_password_hash(form.password.data))
    #insert to db
    try:
      db.session.add(user)
      db.session.commit()
    
      #Log user in
      session['user_id'] = user.id
      flash('Thanks for registering, %s!' % user.name, category="success")
    except IntegrityError as er:
      flash('We had a problem registering you. The name or email you entered is already taken', category='error-message')
      return redirect(url_for('users.register'))
    except:
      flash('We had a problem registering you. If you continue to get this message please contact your administrator.', category='error-message')
      return redirect(url_for('users.register'))
    
    return redirect(url_for('users.home'))
  return render_template('users/register.html', form=form)

  
@mod.route('/reset/', methods=['GET', 'POST'])
def reset_email():
  """
  Password Reset Email
  """
  form = ResetForm(request.form)
  
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if not user:
      flash('The email %s does not exist!' % form.email.data, category='error-message')
      return redirect(url_for('users.reset_email'))
    
    #generate email msg and token
    msg, token = reset_msg(user)
    reset = PasswordReset(email=user.email, s_token=token)
    reset.user = user
    
    try: 
      #Add to db
      db.session.add(reset)
      db.session.commit()
      mail.send(msg)
      flash('A reset password has been sent to %s' % user.email, category='success')
    except:
      flash('There was a error in sending you a email. If this problem persists please contact the admin', category='error-message')
  return render_template('users/reset.html', form=form)
 
#HAVING PROBLEMS HERE
@mod.route('/reset/id/<token>', methods=['GET', 'POST'])
def reset_pw(token=None):
  """
  Password Reset
  """
  form = NewPasswordForm(request.form)
  if request.method == 'POST':
    reset = PasswordReset.query.filter_by(s_token=token).first()
    user = reset.user
  if form.validate_on_submit():
    user.password = generate_password_hash(form.new_password.data)
    db.session.commit()
    flash('Your password has been changed %s' % reset.s_token, category='success')
    return redirect(url_for('users.login'))
  return render_template('users/newpass.html', form=form)
 
 
@mod.route('/new-incentive/', methods=['GET', 'POST'])
@requires_login
def new_incentive():
  """
  Incentive Form
  """
  form = IncentiveForm(request.form)
  if form.validate_on_submit():
    #Create new incentive request form object
    u = User.query.get(session['user_id'])
    incentives = Incentive(date=form.date.data, payable_to=form.payable_to.data, client=form.client.data, opp_name=form.opp_name.data, dec_project=form.dec_project.data, po_num=form.po_num.data, ammount=form.amount.data, requested_by=form.requested_by.data)
    incentives.user = u
   
    #Send email
    msg = msgr(u, incentives)
    
    try:
      mail.send(msg)
      #Add to db
      db.session.add(incentives)
      db.session.commit()
      flash('Incentive request submitted for project %s!' % incentives.dec_project, category="success")
    except AssertionError as er:
      flash('Failed to send mail: %s\nIf this problem persists please contact your admin.' % er, category="error-message")
    except:
      flash('Failed to send mail.\nIf this problem persists please contact your admin.', category="error-message")

    return redirect(url_for('users.get_incentive'))
  return render_template('users/incentive.html', form=form, user=g.user)

  
@mod.route('/past-incentive/')
@requires_login
@get_incentives
def get_incentive():
  """
  Query DB for all posted incentives by user
  """
  return render_template('users/past.html', user=g.user, incentives=g.incentives)
