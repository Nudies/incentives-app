from functools import wraps
from flask import g, flash, redirect, url_for, request
from app.users.models import User, Incentive

def requires_login(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if g.user is None:
      return redirect(url_for('users.login', next=request.path))
    return f(*args, **kwargs)
  return decorated_function
  
def get_incentives(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    incentives = g.user.incentives.all()
    if g.incentives is None:
      g.incentives = incentives[::-1]
    return f(*args, **kwargs)
  return decorated_function