# -*- coding: utf-8 -*-
__version__ = '0.5'

from flask import Flask
from flask import session, g
from flask import (render_template, url_for)
from flask import redirect, make_response, Flask
from flask import Response, jsonify
from flask import abort, request
import pickle
from datetime import timedelta
from uuid import uuid4
from redis import Redis
from redis import StrictRedis
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from json import dumps

import os
import logging
import hashlib
import uuid
from random import randint

app = Flask('app')
app.debug = True

from redis import Redis
redis = Redis()

import os

import rethinkdb as r
from rethinkdb import *
import psycopg2


import logging
logging.basicConfig(filename='TaskWangu.log', level=logging.DEBUG)
salt = 'd40037e1ff7841838235533d910bbf24'


RDB_HOST = os.environ.get('RDB_HOST') or '188.226.195.158'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
LINK_DB = 'LinkUs'


conn_string = "host='188.226.195.158' dbname='LinkUs' user='synod' password='j633.125**//'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()


ONLINE_LAST_MINUTES = 5

app.config[ONLINE_LAST_MINUTES] = 720

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


"""
# mark users online
@app.before_request
def mark_current_user_online():
    mark_online(request.remote_addr)
"""


@app.before_request
def before_request():
    try:
        logging.info('before_request')
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=LINK_DB)
    except RqlDriverError:
        abort(503, "No database connection could be established")


@app.teardown_request
def teardown_request(exception):
    try:
        logging.info('teardown_request')
        g.rdb_conn.close()
    except AttributeError:
        pass

from userOps import *
from taskOps import *
