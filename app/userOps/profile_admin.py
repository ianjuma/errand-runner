#! /usr/bin/env python
# -*- coding: utf-8 -*-

# res/ rep cycle

from app import app
from app import r
from app import g
from app import logging
from app import salt
#from app import cursor
from app import RqlError
from app import session

from flask import (render_template, json, redirect)
from flask import make_response
from flask import jsonify
from flask import abort, request

import hashlib
from random import randint

from mail import sendMail


@app.route('/profile/<username>/', methods=['POST', 'GET'])
def profile(username):
    if session[username] is None:
        return redirect('/')

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
        'PROFILE22.html', name=name, email=email, smscode=smscode,
        state=state, username=username, mobileNo=mobileNo)


@app.route('/payments/<username>/', methods=['POST', 'GET'])
def payments(username):
    if session[username] is None:
        return redirect('/')

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

    if session[username] is None:
        return redirect('/')

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

    username = request.json.get('username')

    if session[username] is None:
        return redirect('/')

    # get JSON params
    fname = request.json.get('fname')
    lname = request.json.get('lname')
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
    if session[username] is None:
        return redirect('/')

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


@app.route('/reset/', methods=['POST', 'GET'])
def forgotPassword():
    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        email = request.json.get('email')

        try:
            user = r.table('UsersInfo').filter(
                {"email": email}).limit(1).pluck('username').run(g.rdb_conn)
            if user is None:
                resp = make_response(jsonify({'Missing': 'Not Found'}), 400)
                resp.headers['Content-Type'] = "application/json"
                resp.cache_control.no_cache = True
                return resp

            new_password = randint(10000, 99999)
            new_password = str(new_password)
            hashed_password = hashlib.sha512(new_password + salt).hexdigest()
            data = []

            for el in user:
                data.append(el)

            username = data[0]['username']

            r.table('UsersInfo').get(
                username).update({"password": hashed_password}).run(g.rdb_conn)

            sendMail.passwordReset(email, new_password)

        except RqlError:
            logging.warning('DB pass reset failed on /reset/')

        resp = make_response(jsonify({'OK': 'Email Sent'}), 200)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template('forgot-pass.html')
