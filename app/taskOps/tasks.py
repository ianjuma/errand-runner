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
import pickle
from datetime import timedelta
from uuid import uuid4
from redis import Redis
from redis import StrictRedis
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from json import dumps

import os
import hashlib
import uuid
from random import randint

import time
from datetime import datetime


@app.route('/tasks/<username>/', methods=['POST', 'GET'])
def tasks(username):
    # task = RegistrationForm(request.form)
    # get mobileNo
    # check if no exists
    return render_template('createTask.html', username=username)


@app.route('/adminTasks/', methods=['POST', 'GET'])
def getAdminTasks():
    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        username = request.json.get('username')
        mobileNo = request.json.get('mobileNo')

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


@app.route('/allTasks/<username>/', methods=['POST', 'GET'])
def getAllTasks(username):
    username = username
    return render_template('allTasks2.html', username=username)


@app.route('/api/getTasks/', methods=['POST', 'GET'])
def getTasks():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    username = request.json.get('username')

    taskData = []
    try:
        tasks = r.table('Tasks').filter({"username": username}).run(g.rdb_conn)
        for data in tasks:
            taskData.append(data)

    except RqlError:
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


@app.route('/editTask/<username>/<task_id>/')
def taskInfo(username, task_id):
    try:
        user = r.table('Tasks').get(task_id).run(g.rdb_conn)

        task_title = str(user['task_title'])
        task_desc = str(user['task_desc'])
        task_urgency = str(user['task_urgency'])
        task_category = str(user['task_category'])
        due_date = str(user['due_date'])

    except RqlError:
        logging.warning('DB operation failed on /editTask/<task_id>/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template(
        'editTask2.html', task_category=task_category, task_urgency=task_urgency,
        task_desc=task_desc, task_title=task_title, due_date=due_date, username=username, task_id=task_id)


@app.route('/api/editTask/<task_id>/', methods=['PUT', 'POST'])
def editTask(task_id):
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    task_urgency = request.json.get('urgency')
    task_title = request.json.get('title')
    task_desc = request.json.get('description')
    task_category = request.json.get('category')
    due_date = request.json.get('due_date')
    task_id = request.json.get('task_id')

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
                                          'task_category': task_category, 'task_urgency': task_urgency,
                                          'due_date': due_date}).run(g.rdb_conn)

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


@app.route('/api/deleteTask/', methods=['PUT', 'POST'])
def deleteTask():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    task_id = request.json.get('task_id')

    try:
        # r.table('UsersInfo').get(mobileNo).update({"smscode": SMScode}).run(g.rdb_conn)
        r.table('Tasks').get(task_id).delete().run(g.rdb_conn)
    except RqlError:
        logging.warning('DB code verify failed on /api/deleteTask/')
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

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    username = request.json.get('username')
    task_desc = request.json.get('description')
    task_title = request.json.get('title')
    # then update userInfo
    task_category = request.json.get('category')
    task_urgency = request.json.get('urgency')
    due_date = request.json.get('due_date')

    taskData = {"username": username, "task_title": task_title, "task_desc": task_desc,
                "task_category": task_category, "task_urgency": "started", "due_date": due_date}

    text_all = "LinkUs new task -> " + task_title + task_desc

    try:
        r.table('Tasks').insert(taskData).run(g.rdb_conn)
    except RqlError:
        logging.warning('DB code verify failed on /api/addTask/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    # send email and SMS notification
    # sendText("+254710650613", str(text_all))
    # send_message("khalifleila@gmail.com", str(taskData))

    resp = make_response(jsonify({"OK": "Task Created"}), 200)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp
