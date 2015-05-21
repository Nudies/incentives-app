from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from app import db
from app.users.forms import RegisterForm, LoginForm, IncentiveForm
from app.users.models import User, Incentive
from app.users.decorators import requires_login, get_incentives

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
      flash('Welcome back, %s!' % user.name, category="success")
      return redirect(url_for('users.home'))
    flash('Wrong email or password', 'error-message')
  return render_template('users/login.html', form=form)
 
@mod.route('/logout/')
def logout():
  """
  Drops user session
  """
  session.pop('user_id', None)
  flash('You were successfully logged out!', category="success")
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
    db.session.add(user)
    db.session.commit()
    
    #Log user in
    session['user_id'] = user.id
    flash('Thanks for registering, %s' % user.name, category="success")
    return redirect(url_for('users.home'))
  return render_template('users/register.html', form=form)
  
 
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
    incentives = Incentive(date=form.date.data, payable_to=form.payable_to.data,
            client=form.client.data, opp_name=form.opp_name.data,
            dec_project=form.dec_project.data, po_num=form.po_num.data,
            ammount=form.amount.data, requested_by=form.requested_by.data)
    incentives.user = u
    #Add to db
    db.session.add(incentives)
    db.session.commit()
    
    #User feedback
    flash('Incentive request submitted for project %s!' % incentives.dec_project, category="success")
    return redirect(url_for('users.home'))
  return render_template('users/incentive.html', form=form, user=g.user)
  
@mod.route('/past-incentive/')
@requires_login
@get_incentives
def get_incentive():
  """
  Query DB for all posted incentives by user
  """
  return render_template('users/profile.html', user=g.user, incentives=g.incentives)
