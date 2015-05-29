#!/usr/bin/env python
import os
from pprint import pprint
from flask import *
from app import *
from app import db
from app.users.models import User, Incentive
"""
db.create_all()
"""
os.environ['PYTHONINSPECT'] = 'True'
