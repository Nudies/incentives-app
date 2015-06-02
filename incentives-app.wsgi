#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/incentives-app/")

from app import app as application
application.secret_key = 'ash23jhshaskh312kh123'
