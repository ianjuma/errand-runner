# -*- coding: utf-8 -*-
__version__ = '0.1.8'

from flask import Flask
from flask import session, g, request
from flask import (url_for, redirect)
from flask import abort
from functools import wraps

import os
import logging


app = Flask('app')
app.debug = True

import rethinkdb as r
from rethinkdb import *

logging.basicConfig(filename='TaskWangu.log', level=logging.DEBUG)
salt = 'd40037e1ff7841838235533d910bbf24'


RDB_HOST = os.environ.get('RDB_HOST') or '127.0.0.1'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
LINK_DB = 'LinkUs'


import requests
import simplejson

# import psycopg2
# conn_string = "host='188.226.195.158' dbname='LinkUs' user='synod' password='db_pass'"
# conn = psycopg2.connect(conn_string)
# cursor = conn.cursor()

ONLINE_LAST_MINUTES = 5

app.config[ONLINE_LAST_MINUTES] = 720
app.secret_key = 'I\xf9\x9cF\x1e\x04\xe6\xfaF\x8f\xe6)-\xa432'

from datetime import timedelta
app.permanent_session_lifetime = timedelta(minutes=5760)


def dbSetup():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(LINK_DB).run(connection)
        r.db(LINK_DB).table_create('User').run(connection)
        logging.info('Database setup completed')
    except RqlRuntimeError:
        logging.info('App database already exists')
    finally:
        connection.close()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if username not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def before_request():
    try:

        if 'username' not in request.cookies:
            redirect('/')

        logging.info('before_request')
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=LINK_DB)
    except RqlDriverError:
        """
        log_data = "LOG_INFO=" + simplejson.dumps(
        {
           'Request':'app.before failed database',
        })
        requests.post("https://logs-01.loggly.com/inputs/e15fde1a-fd3e-4076-a3cf-68bd9c30baf3/tag/python/", log_data)
        """

        abort(503, "No database connection could be established")


@app.teardown_request
def teardown_request(exception):
    try:
        logging.info('teardown_request')
        g.rdb_conn.close()
    except AttributeError:
        logging.info('Database failure - check your connection')

from userOps import *
from taskOps import *
