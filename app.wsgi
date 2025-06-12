import sys
import os
sys.path.insert(0,'/home/sugrp202/public_html')

activate_this = '/home/sugrp202/VIRTENV/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import app as application


#https://www.youtube.com/watch?v=w0QDAg85Oow