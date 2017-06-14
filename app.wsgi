#! .env/bin/python
activate_this = '/var/www/html/blocknav.io/.env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import os
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/blocknav.io/')

from app import app as application
application.secret_key = os.urandom(10)