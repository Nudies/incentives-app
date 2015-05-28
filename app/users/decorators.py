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
    if (g.user.role == 0 or g.user.role == 1) and g.incentives is None:
      g.incentives = Incentive.query.all()[::-1]
      return f(*args, **kwargs)
    else:
      incentives = g.user.incentives.all()
      if g.incentives is None:
        g.incentives = incentives[::-1]
      return f(*args, **kwargs)
  return decorated_function