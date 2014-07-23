#! /usr/bin/env python
# -*- coding: utf-8 -*-

# res/ rep cycle

from app import app
from app import r
from app import g
from app import logging
from app import salt
from app import cursor

from flask import (render_template)
from flask import redirect, make_response
from flask import Response, jsonify
from flask import abort, request
from flask import session, g
from datetime import timedelta
from json import dumps

import os
import logging
import hashlib

import time
from datetime import datetime


@app.route('/profile/<username>/', methods=['POST', 'GET'])
def profile(username):

    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        password = request.json.get('password')
        smsdata = request.json.get('smsdata')
        email = request.json.get('email')
        dob = request.json.get('dob')
        username = request.json.get('username')
        state = request.json.get('state')
        mobileNo = request.json.get('mobileNo')

        if mobileNo.startswith('0'):
            mobileNo = mobileNo[1:]

        if mobileNo.startswith('+254'):
            mobileNo = mobileNo[4:]

        try:
            user = r.table(
                'UsersInfo').get(str(username)).update({"email": email, "smscode": smsdata,
                                                        "state": state, "dob": dob, "mobileNo": mobileNo}).run(g.rdb_conn)

            resp = make_response(jsonify({"OK": "User Updated"}), 202)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        except RqlError:
            logging.warning(
                'DB code verify failed on /profile/api/' + username)
            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

    try:
        user = r.table('UsersInfo').get(str(username)).run(g.rdb_conn)

        name = str(user['username'])
        state = str(user['state'])
        smscode = str(user['smscode'])
        password = str(user['password'])
        email = str(user['email'])
        mobileNo = str(user['mobileNo'])

    except RqlError:
        logging.warning('DB code verify failed on /profile/' + mobileNo)
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template(
        'profile2.html', name=name, email=email, smscode=smscode,
        state=state, username=username, mobileNo=mobileNo)



@app.route('/payments/<username>/', methods=['POST', 'GET'])
def payments(username):

    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        password = request.json.get('password')
        smsdata = request.json.get('smsdata')
        email = request.json.get('email')
        dob = request.json.get('dob')
        username = request.json.get('username')
        state = request.json.get('state')
        mobileNo = request.json.get('mobileNo')

        if mobileNo.startswith('0'):
            mobileNo = mobileNo[1:]

        if mobileNo.startswith('+254'):
            mobileNo = mobileNo[4:]

        try:
            user = r.table(
                'UsersInfo').get(str(username)).update({"email": email, "smscode": smsdata,
                                                        "state": state, "dob": dob, "mobileNo": mobileNo}).run(g.rdb_conn)

            resp = make_response(jsonify({"OK": "User Updated"}), 202)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        except RqlError:
            logging.warning(
                'DB code verify failed on /profile/api/' + username)
            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

    try:
        user = r.table('Payments').get(str(username)).run(g.rdb_conn)
        username = str(user['username'])
        credit = str(user['credit_available'])

    except RqlError:
        logging.warning('DB code verify failed on /payments/' + mobileNo)
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template(
        'payments.html', username=username, credit=credit)


@app.route('/api/removeUser/', methods=['POST'])
def removeUser():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    password = request.json.get('password')
    username = request.json.get('username')

    # mobile no is the id - primary key
    try:
        r.table('UsersInfo').get(username).delete().run(g.rdb_conn)
    except RqlError:
        logging.warning('DB remove user failed on /api/removeUser')

    resp = make_response(jsonify({'OK': 'Content Removed'}), 202)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/UserInfo/', methods=['POST'])
def addUser():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    # get JSON engine params
    fname = request.json.get('fname')
    lname = request.json.get('lname')
    username = request.json.get('username')
    mobileNo = request.json.get('mobileNo')  # this <- id
    state = request.json.get('state')
    location = request.json.get('location')
    email = request.json.get('email')

    # no id just work with mobileNo - easier
    # we'll send a text message enter code!

    if mobileNo.startswith('0'):
        mobileNo = mobileNo[1:]

    if mobileNo.startswith('+254'):
        mobileNo = mobileNo[4:]

    try:
        r.table('UsersInfo').insert({
            'fname': fname,
            'lname': lname,
            'mobileNo': mobileNo,
            'email': email,
            'state': state,
            'userVerified': 'False',
            'location': location
        }).run(g.rdb_conn)
    except RqlError:
        logging.warning('DB could not write on /api/adduser')

    resp = make_response(jsonify({"OK": "Content Saved"}), 202)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


# credit API
@app.route('/api/credit/<username>/', methods=['POST', 'GET'])
def credit(username):

    if request.method == 'GET':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        password = request.json.get('password')
        username = request.json.get('username')

        try:
            user = r.table(
                'Payments').get(str(username)).pluck('credit_available').run(g.rdb_conn)

            credit = json.dumps(user)
            resp = make_response(jsonify(credit), 202)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        except RqlError:
            logging.warning(
                'DB code verify failed on /api/credit' + username)
            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        password = request.json.get('password')
        username = request.json.get('username')

        try:
            user = r.table(
                'Payments').get(str(username)).pluck('credit_available').run(g.rdb_conn)

            resp = make_response(jsonify({"OK": "User Updated"}), 202)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        except RqlError:
            logging.warning(
                'DB code verify failed on /api/credit' + username)
            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

