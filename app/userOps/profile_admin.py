#! /usr/bin/env python
# -*- coding: utf-8 -*-

# res/ rep cycle

from app import app
from app import r
from app import g
from app import logging
from app import salt
from app import RqlError
from app import session

from flask import (render_template, json, redirect)
from flask import make_response
from flask import jsonify
from flask import abort, request

import hashlib
from random import randint

from mail import sendMail
import urllib


@app.route('/profile/', methods=['POST', 'GET'])
def profile():
    #if session[username] is None:
    #    return redirect('/')
    
    #if username not in session:
    #    return redirect('/')


    if 'username' not in request.cookies:
        return redirect('/')

    if request.cookies.get('username') == '' or request.cookies.get('username') is None:
        return redirect('/')

    username = request.cookies.get('username')


    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
            abort(400)

        password = request.json.get('password')
        email = request.json.get('email')
        dob = request.json.get('dob')
        username = request.json.get('username')
        firstname = request.json.get('firstname')
        lastname = request.json.get('lastname')
        state = request.json.get('state')
        mobileNo = request.json.get('mobileNo')

        if mobileNo.startswith('0'):
            mobileNo = mobileNo[1:]

        if mobileNo.startswith('+254'):
            mobileNo = mobileNo[4:]

        try:
            user = r.table(
                'UsersInfo').get(str(username)).update({"email": email, "lname": lastname, "fname": firstname,
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
        #password = str(user['password'])
        email = str(user['email'])
        mobileNo = str(user['mobileNo'])
        firstname = str(user['fname'])
        lastname = str(user['lname'])

    except RqlError:
        logging.warning('DB code verify failed on /profile/' + mobileNo)
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp


    # profile url fix - only on signUp
    default_url = "http://www.gravatar.com/avatar"
    size = 80
    profile_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    profile_url += urllib.urlencode({'d':default_url, 's':str(size)})

    return render_template(
        'Profile.html', name=name, lastname=lastname, firstname=firstname, email=email, smscode=smscode,
        state=state, username=username, mobileNo=mobileNo, profile_image=profile_url)


@app.route('/payments/', methods=['POST', 'GET'])
def payments():
    #if session[username] is None:
    #    return redirect('/')

    #if username not in session:
    #    return redirect('/')

    if 'username' not in request.cookies:
        return redirect('/')

    if request.cookies.get('username') == '' or request.cookies.get('username') is None:
        return redirect('/')

    username = request.cookies.get('username')

    # session is a list object
    #try:
    #    username = session['username']
    #except KeyError:
    #    return redirect('/')


    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
            abort(400)

        email = request.json.get('email')
        dob = request.json.get('dob')
        state = request.json.get('state')
        mobileNo = request.json.get('mobileNo')

        if mobileNo.startswith('0'):
            mobileNo = mobileNo[1:]

        if mobileNo.startswith('+254'):
            mobileNo = mobileNo[4:]

        try:
            user = r.table(
                'UsersInfo').get(str(username)).update({"email": email, "state": state,
                                "dob": dob, "mobileNo": mobileNo}).run(g.rdb_conn)

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

    if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
        abort(400)

    password = request.json.get('password')
    username = request.json.get('username')

    #if session[username] is None:
    #    return redirect('/')
    if username not in session:
        return redirect('/')


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
        logging.warning('Wrong password user failed on /api/signIn/')


    session.pop(username, None)

    try:
        r.table('UsersInfo').get(username).delete().run(g.rdb_conn)
    except RqlError:
        logging.warning('DB remove user failed on /api/removeUser')

    resp = make_response(jsonify({'OK': 'User Deleted'}), 202)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/UserInfo/', methods=['POST'])
def addUser():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
        abort(400)

    username = request.json.get('username')

    #if session[username] is None:
    #    return redirect('/')
    if username not in session:
        return redirect('/')

    # get JSON params
    fname = request.json.get('fname')
    lname = request.json.get('lname')
    mobileNo = request.json.get('mobileNo')
    state = request.json.get('state')
    location = request.json.get('location')
    email = request.json.get('email')


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
    #if session[username] is None:
    #    return redirect('/')
    if username not in session:
        return redirect('/')

    if request.method == 'GET':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
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

        if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
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

        if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
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
