#!/usr/bin/python
import sys, logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Project_Watchdogs/flask/watchdogs/")

from app import app as application
application.secret_key = "123412351235235"