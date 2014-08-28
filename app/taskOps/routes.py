#! /usr/bin/env python
# -*- coding: utf-8 -*-

# res/ rep cycle

from app import app
from app import r
from app import g
from app import logging
from app import salt
from app import red
from app import RqlError

from flask import (render_template)
from flask import redirect, make_response
from flask import jsonify
from flask import abort, request
from flask import session

import hashlib
from random import randint

secret_key = app.secret_key

from mail import sendMail
from payments import process_payments


@app.route('/admin/', methods=['POST', 'GET'])
def adminSign():
    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
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

        session[username] = username

        resp = make_response(jsonify({"OK": "Signed In"}), 200)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template('adminSignin.html')


@app.route('/api/signIn/', methods=['POST', 'PUT'])
def signIn():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
        abort(400)

    session.permanent = True

    password = request.json.get('password')
    username = request.json.get('username')

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
    session[username] = username


    resp = make_response(jsonify({"OK": "Signed In"}), 200)
    resp.headers['Content-Type'] = "application/json"
    resp.set_cookie('username',value=username)

    resp.cache_control.no_cache = True
    return resp


@app.route('/api/signUp/', methods=['POST'])
def getRandID():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
        abort(400)

    # use the mobile number as the id number its a unique entity
    # it works :D
    # use mobile number as username upon login -> send text with code
    username = request.json.get('username')
    email = request.json.get('email')
    # then update userInfo
    password = request.json.get('password')
    email = str(email)
    username = str(username)

    try:
        user = r.table('UsersInfo').get(username).run(g.rdb_conn)
        if user is not None:
            resp = make_response(jsonify({"Error": "User Exists"}), 400)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        user = r.table('UsersInfo').filter({"email": email}).limit(1).run(g.rdb_conn)
        userData =[]

        for data in user:
            userData.append(data)

        if userData != []:
            resp = make_response(jsonify({"Error": "User Email Exists"}), 400)
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

    # @task sendMail
    try:
        sendMail.sendMail(email, SMScode, username)
    except URLError:
        logging.warning('sendMail verify failed on /api/signUp/')
        abort(500)
    except Exception, e:
        logging.warning('SendMail error on /api/signUp/ %s' %(e) )


    # verify user send email with code
    # sendText(mobileNo, SMScode)
    hashed_password = hashlib.sha512(password + salt).hexdigest()

    try:
        # r.table('UsersInfo').get(mobileNo).update({"smscode": SMScode}).run(g.rdb_conn)
        r.table(
            'UsersInfo').insert({"state": "", "fname": "", "lname": "" ,"username": username, "dob": "", 
            "email": email, "password": hashed_password, "smscode": SMScode, "mobileNo": ""}).run(g.rdb_conn)
    except RqlError:
        # payload = "LOG_INFO=" + simplejson.dumps({ 'Sign Up':'Sign Up Failed' })
        # requests.post("https://logs-01.loggly.com/inputs/e15fde1a-fd3e-4076-a3cf-68bd9c30baf3/tag/python/", payload)

        logging.warning('DB code verify failed on /api/signUp/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    # add to sessions then login
    session[username] = username
    # return redirect()

    resp = make_response(jsonify({"OK": "Signed Up"}), 202)
    resp.set_cookie('username',value=username)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/newsLetter/', methods=['POST'])
def addNewsLetter():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
        abort(400)

    if 'username' not in request.cookies:
        return redirect('/')

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


@app.route('/logout/', methods=['GET'])
def logout():
    # remove from session and clear cookie
    if 'username' not in request.cookies:
        return redirect('/')

    username = request.cookies.get('username')
    session.pop(username, None)

    resp = make_response( redirect('/') )
    resp.set_cookie('username', '', expires=0)
    return resp


@app.route('/confirm/<smscode>/', methods=['PUT', 'POST'])
def confirmUser(smscode):
    # make request to get one task
    #if session[username] is None:
    #    return redirect('/')

    #if username not in session:
    #    return redirect('/')


    if 'username' not in request.cookies:
        return redirect('/')

    username = request.cookies.get('username')


    try:
        user = r.table(
            'UsersInfo').get(username).pluck('smscode').run(g.rdb_conn)
    except RqlError:
        # payload = "LOG_INFO=" + simplejson.dumps({ 'Confirmation Error':'Email Confirm Failed' })
        # requests.post("https://logs-01.loggly.com/inputs/e15fde1a-fd3e-4076-a3cf-68bd9c30baf3/tag/python/", payload)

        logging.warning('DB op failed on /confirmUser/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    if str(user) is not str(smscode):
        return
        """
        EMAIL VERFICATION FAILED
        """

    return redirect("/task/createTask/", code=302)


@app.route('/post_payment/', methods=['GET', 'POST'])
def post_payment_pesapal():
    #if username not in session:
    #    return redirect('/')

    if 'username' not in request.cookies:
        return redirect('/')

    username = request.cookies.get('username')
    # with ref set in rand generator
    pesapal_merchant_ref = request.args.get('pesapal_merchant_reference')
    pesapal_merchant_id  = request.args.get('pesapal_transaction_tracking_id')

    # store merchant info in db
    # basic post_payment page TO LOAD
    pesapal_data = { "pesapal_transaction_tracking_id": pesapal_merchant_id, 
        "pesapal_merchant_reference": pesapal_merchant_ref, "username": username }

    try:
        r.table('Payments').insert(pesapal_data).run(g.rdb_conn)
    except Exception:
        logging.warning('DB code verify failed on /post_payment/')

        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    # optional get payment status - info sent to pesapla ipn notification
    # per user info - render post payment page - by merchant ref
    """
    post_params = {
      'pesapal_merchant_reference': '000',
      'pesapal_transaction_tracking_id': '000'
    }
    """

    status = process_payments.queryPaymentByRef(pesapal_data)
    return render_template('PostPayment.html', status=status, username=username)


@app.route('/pesapal_ipn_notification/', methods=['POST'])
def ipn_notify():
    #url = request.get.args('url')
    # compare with merchant ref
    pesapal_merchant_ref = request.args.get('pesapal_merchant_reference')
    pesapal_merchant_id  = request.args.get('pesapal_transaction_tracking_id')

    # store in db per user info in payments

    resp = make_response(jsonify({"OK": "Notification Received"}), 200)
    resp.cache_control.no_cache = True
    return resp


@app.route('/process_payments/', methods=['GET'])
def process_payment():
    #if username not in session:
    #    return redirect('/')

    if 'username' not in request.cookies:
        return redirect('/')

    if request.cookies.get('username') == '' or request.cookies.get('username') is None:
        return redirect('/')

    username = request.cookies.get('username')

    # fetch url from redis - attach iframe to window
    url = red.hget(username, 'url')
    return render_template('pesapal_payment.html', username=username, iframe=url)