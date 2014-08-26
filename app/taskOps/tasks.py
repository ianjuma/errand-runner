#! /usr/bin/env python
# -*- coding: utf-8 -*-

# res/ rep cycle

from app import app
from app import r
from app import g
from app import logging
from app import red
from app import RqlError
from app import session

from flask import (render_template, redirect, url_for)
from flask import make_response
from flask import jsonify
from random import randint
from flask import abort, request

from json import dumps

from mail import sendMail
from mail import messageAPI
from payments import process_payments


from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in request.cookies:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@login_required
@app.route('/task/createTask/', methods=['POST', 'GET'])
def tasks():

    #if username not in session:
    #    return redirect('/')

    if 'username' not in request.cookies:
        return redirect('/')

    # use redis sessions with ttl

    if request.cookies.get('username') == '' or request.cookies.get('username') is None:
        return redirect('/')

    username = request.cookies.get('username')
    return render_template('CREATEtask.html', username=username)


@app.route('/adminTasks/', methods=['GET'])
def getAdminTasks():
    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
            abort(400)

        
        # add to sessions then login
        #if username not in session:
        #    return redirect('/')

        #print request.cookies
        if 'username' not in request.cookies:
            return redirect('/')

        username = request.cookies.get('username')
        if request.cookies.get('username') == '' or request.cookies.get('username') is None:
            return redirect('/')


        taskData = []
        try:
            tasks = r.table('Tasks').filter(
                {'task_urgency': 'started'}).limit(50).run(g.rdb_conn)
            for data in tasks:
                taskData.append(data)

        except RqlError:
            logging.warning('DB code verify failed on /api/adminTasks/')
            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        taskData = dumps(taskData)

        resp = make_response(taskData, 200)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    try:
        task_size = r.table('Tasks').count().run(g.rdb_conn)

    except RqlError:
        logging.warning('DB code verify failed on /api/adminTasks/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template('adminViewTasks.html', task_size=task_size)


@app.route('/task/myTasks/', methods=['POST', 'GET'])
def getAllTasks():
    # wrong session - keyerror fail
    #if session[str(username)] is None:
    #    return redirect('/')

    #if username not in session:
    #    return redirect('/')

    if 'username' not in request.cookies:
        return redirect('/')

    if request.cookies.get('username') == '' or request.cookies.get('username') is None:
        return redirect('/')

    username = request.cookies.get('username')

    return render_template('VIEWtasks.html', username=username)


@login_required
@app.route('/api/getTasks/', methods=['POST', 'GET'])
def getTasks():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
        abort(400)

    username = request.json.get('username')

    #if session[username] is None:
    #    return redirect('/')
    if username not in session:
        return redirect('/')

    taskData = []
    try:
        tasks = r.table('Tasks').filter({"username": username}).run(g.rdb_conn)
        for data in tasks:
            taskData.append(data)

    except RqlError:
        #payload = "LOG_INFO=" + simplejson.dumps({ 'Request':'app.before' })
        #requests.post("https://logs-01.loggly.com/inputs/e15fde1a-fd3e-4076-a3cf-68bd9c30baf3/tag/python/", payload)

        logging.warning('DB code verify failed on /api/getTasks/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    taskData = dumps(taskData)

    resp = make_response(taskData, 200)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/task/editTask/<task_id>/', methods=['GET'])
def taskInfo(task_id):
    #if session[username] is None:
    #    return redirect('/')

    #if username not in session:
    #    return redirect('/')

    if 'username' not in request.cookies:
        return redirect('/')

    if request.cookies.get('username') == '' or request.cookies.get('username') is None:
        return redirect('/')

    username = request.cookies.get('username')

    try:
        user = r.table('Tasks').get(task_id).run(g.rdb_conn)

        task_title = str(user['task_title'])
        task_desc = str(user['task_desc'])
        task_urgency = str(user['task_urgency'])
        task_category = str(user['task_category'])
        due_date = str(user['due_date'])
        contactPersons = str(user['contactPersons'])
        location = str(user['locationData'])


    except RqlError:
        #payload = "LOG_INFO=" + simplejson.dumps({ '/editTask/<username>/<task_id>/':'DB operation failed on /editTask/<task_id>/' })
        #requests.post("https://logs-01.loggly.com/inputs/e15fde1a-fd3e-4076-a3cf-68bd9c30baf3/tag/python/", payload)

        logging.warning('DB operation failed on /editTask/<task_id>/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template(
        'EditTask.html', task_category=task_category, task_urgency=task_urgency, locationData=location, contactPersons=contactPersons,
        task_desc=task_desc, task_title=task_title, due_date=due_date, username=username, task_id=task_id)


@app.route('/api/editTask/<task_id>/', methods=['PUT', 'POST'])
def editTask(task_id):
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
        abort(400)

    username = request.json.get('username')
    #if session[username] is None:
    #    return redirect('/')

    if username not in session:
        return redirect('/')

    task_urgency = request.json.get('task_urgency')
    task_title = request.json.get('title')
    task_desc = request.json.get('description')
    # task_category = request.json.get('category')
    due_date = request.json.get('due_date')
    task_id = request.json.get('task_id')
    locationData = request.json.get('locationData')
    contactPersons = request.json.get('contactPersons')

    # make request to get one task
    if request.method == 'GET':
        try:
            user_task = r.table('Tasks').get(task_id).run(g.rdb_conn)

        except RqlError:
            logging.warning('DB op failed on /api/editTask/')
            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        resp = make_response(jsonify({"Task fetched": user_task}), 202)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    try:
        r.table(
            'Tasks').get(task_id).update({'task_desc': task_desc, 'task_title': task_title,
                                          'task_urgency': task_urgency,
                                          'due_date': due_date, "locationData": locationData, 
                                          'contactPersons': contactPersons }).run(g.rdb_conn)

    except RqlError:
        logging.warning('DB code verify failed on /api/editTask/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    resp = make_response(jsonify({"OK": "Task Updated"}), 202)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/deleteTask/', methods=['PUT', 'POST', 'DELETE'])
def deleteTask():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
        abort(400)

    username = request.json.get('username')
    #if session[username] is None:
    #    return redirect('/')

    if username not in session:
        return redirect('/')

    task_id = request.json.get('task_id')


    try:
        r.table('Tasks').get(task_id).delete().run(g.rdb_conn)
    except RqlError:
        logging.warning('DB code verify failed on /api/deleteTask/')

        #payload = "LOG_INFO=" + simplejson.dumps({ '/editTask/<username>/<task_id>/':'DB operation failed on /editTask/<task_id>/' })
        #requests.post("https://logs-01.loggly.com/inputs/e15fde1a-fd3e-4076-a3cf-68bd9c30baf3/tag/python/", payload)
        
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    resp = make_response(jsonify({"OK": "Task Deleted"}), 200)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/addTask/', methods=['POST', 'GET'])
def addTask():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json; charset=UTF-8':
        abort(400)

    username = request.json.get('username')
    #if session[username] is None:
    #    return redirect('/')
    if username not in session:
        return redirect('/')

    task_desc = request.json.get('description')
    task_title = request.json.get('title')
    # then update userInfo
    task_category = request.json.get('category')
    task_urgency = request.json.get('urgency') # checkbox
    due_date = request.json.get('due_date')
    locationData = request.json.get('locationData')
    contactPersons = request.json.get('contactPersons')

    # unpaid status - pending - started - finished
    taskData = { "username": username, "task_title": task_title, "task_desc": task_desc, "locationData": locationData,
                "task_category": task_category, "task_urgency": "UNPAID", "due_date": due_date, "contactPersons": contactPersons }

    text_all = "LinkUs new task %s " %(task_title)

    try:
        r.table('Tasks').insert(taskData).run(g.rdb_conn)
    except RqlError:
        logging.warning('DB code verify failed on /api/addTask/')

        #payload = "LOG_INFO=" + simplejson.dumps({ '/api/addTask/':'DB operation failed on /addTask/' })
        #requests.post("https://logs-01.loggly.com/inputs/e15fde1a-fd3e-4076-a3cf-68bd9c30baf3/tag/python/", payload)

        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    # send email and SMS notification
    # rabbitMQ tasks
    try:
        messageAPI.send_notification_task("+254710650613", str(text_all))
        sendMail.new_task_message("khalifleila@gmail.com", str(taskData), username)
    except Exception:
        logging.warning('Send SMS failed on /api/addTask/ notification failed')


    user_info = r.table('UsersInfo').get(username).pluck('email').run(g.rdb_conn)
    mobileNo = r.table('UsersInfo').get(username).pluck('mobileNo').run(g.rdb_conn)
    email = user_info['email']

    #print email
    # setup URL to payments - user specific data

    merchant_ref = "Ta" + str(randint(10000, 99999)) + "W"
    #merchant_ref = '12erwe'
    request_data = {
        'Amount': '2000',
        'Description': task_title,
        'Type': 'MERCHANT',
        'Reference': merchant_ref,
        'PhoneNumber': mobileNo,
        'Email': email
    }

    print request_data
    url = process_payments.postOrder(request_data)
    print url

    # store URL in redis under username
    # set with expire
    red.hset(username, 'url', url)
    red.expire(username, 300)

    # resp = make_response(redirect(pay_url, code=302))

    resp = make_response(jsonify({"OK": "Task Created"}), 200)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp