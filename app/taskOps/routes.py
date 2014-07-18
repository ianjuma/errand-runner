#! /usr/bin/env python
# -*- coding: utf-8 -*-

# res/ rep cycle

from app import app
from app import r
from app import g
from app import logging
from app import salt
from app import cursor


from flask import (render_template, url_for)
from flask import redirect, make_response, Flask
from flask import Response, jsonify
from flask import abort, request
from flask import session, g
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


import time
from datetime import datetime

from redis import Redis
redis = Redis()

import requests


@app.route('/admin/', methods=['POST', 'GET'])
def adminSign():
    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        username = request.json.get('username')
        password = request.json.get('password')

        try:
            user = r.table('Admin').get(username).run(g.rdb_conn)
        except Exception, e:
            logging.warning('DB failed on /admin/ -> user not found')
            raise e

        if user is None:
            resp = make_response(jsonify({"Not Found": "User Not Found"}), 404)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        resp = make_response(jsonify({"OK": "Signed In"}), 200)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template('adminSignin.html')


@app.route('/api/signIn/', methods=['POST', 'PUT'])
def signIn():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    password = request.json.get('password')
    username = request.json.get('username')
    email = request.json.get('email')

    # join to another table
    try:
        user = r.table('UsersInfo').get(username).run(g.rdb_conn)
    except Exception, e:
        logging.warning('DB signIn failed on /api/signIn/ -> user not found')
        raise e

    if user is None:
        resp = make_response(jsonify({"Not Found": "User Not Found"}), 404)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    hashed_password = hashlib.sha512(str(password) + salt).hexdigest()

    try:
        user = r.table('UsersInfo').get(username).run(g.rdb_conn)

        if str(user['password']) != str(hashed_password):
            # add user to session then log in
            resp = make_response(
                jsonify({"Password": "Incorrect Password"}), 404)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp
    except RqlError:
        logging.warning('raise RqlError DB signIn failed on /api/signIn/')

    # manage sessions - add user to session
    # redis sessions -> flask
    # redis k/v store | dict
    resp = make_response(jsonify({"OK": "Signed In"}), 200)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/signUp/', methods=['POST'])
def getRandID():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    # use the mobile number as the id number its a unique entity
    # it works :D
    # use mobile number as username upon login -> send text with code
    username = request.json.get('username')
    email = request.json.get('email')
    # then update userInfo
    password = request.json.get('password')

    try:
        user = r.table('UsersInfo').get(username).run(g.rdb_conn)
        if user is not None:
            resp = make_response(jsonify({"Error": "User Exists"}), 400)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp
    except RqlError:
        logging.warning('DB code verify failed on /api/signUp/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    SMScode = randint(10000, 99999)
    # verify user send email with code
    # or SMS code
    # sendText(mobileNo, SMScode)
    hashed_password = hashlib.sha512(password + salt).hexdigest()

    try:
        # r.table('UsersInfo').get(mobileNo).update({"smscode": SMScode}).run(g.rdb_conn)
        r.table(
            'UsersInfo').insert({"state": "", "username": username, "dob": "", "email": email, "password": hashed_password,
                                 "smscode": SMScode, "mobileNo": ""}).run(g.rdb_conn)
    except RqlError:
        logging.warning('DB code verify failed on /api/signUp/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    # add to sessions then login

    resp = make_response(jsonify({"OK": "Signed Up"}), 202)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/newsLetter/', methods=['POST'])
def addNewsLetter():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    email = request.json.get('email')
    # mobile no is the id - primary key

    try:
        r.table('newsLetter').insert({
            'email': email,
        }).run(g.rdb_conn)
    except RqlError:
        logging.warning('DB could not write on /api/newsLetter/')
        resp = make_response(jsonify({'Error': 'Save Failed'}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    resp = make_response(jsonify({'OK': 'Content Saved'}), 202)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp