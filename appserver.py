#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Requisitos:
# ------------------------------
# VC++ Compiler for python 2.7
# pip install bottle
# pip install passlib
# pip install mysql-python
# pip install gevent
# pip install bcrypt

from gevent import monkey; monkey.patch_all()

import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('./app')
sys.path.append('./api')
sys.path.append(os.path.dirname(__file__))

import server_entry
import bottle

bottle.TEMPLATE_PATH.append('./static')


bottle.run(host='0.0.0.0', port=8080, server='gevent', debug=True, reloader=True)
