import os
import sys

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

mail = Mail(app)


def install_secret_key(app, filename='key.txt'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(app.instance_path, filename)

    try:
      app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
      print('Error: No secret key. Create it with:')
      full_path = os.path.dirname(filename)
      if not os.path.isdir(full_path):
          print('mkdir -p {filename}'.format(filename=full_path))
      print('head -c 24 /dev/urandom > {filename}'.format(filename=filename))
      sys.exit(1)

if not app.debug:
  install_secret_key(app)
  #import logging
  #from logging.handlers import SMTPHandler
  #mail_handler = SMTPHandler('127.0.0.1', 'server-error@example.com', 'rsiemens@decipherinc.com', 'YourApplication Failed')
  #mail_handler.setLevel(logging.ERROR)
  #app.logger.addHandler(mail_handler)
  
 
@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404
  
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

from app.users.view import mod as usersModule
app.register_blueprint(usersModule)
