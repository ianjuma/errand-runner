# -*- coding: utf-8 -*-
__version__ = '0.4.2'

from flask import Flask
from flask import g, session, request
from flask import (url_for, redirect)
from flask import abort
from functools import wraps

import os
import logging
import settings

app = Flask('app')
app.config.from_pyfile('settings.py', silent=True)

import rethinkdb as r
from rethinkdb import *

import redis
red = redis.StrictRedis(host='localhost', port=6379, db=0)

logging.basicConfig(filename='TaskWangu.log', level=logging.DEBUG)
salt = settings.salt

app.config['ONLINE_LAST_MINUTES'] = settings.ONLINE_LAST_MINUTES
app.secret_key = settings.SECRET_KEY

from datetime import timedelta
app.permanent_session_lifetime = timedelta(minutes=5760)


from celery import Celery
from crons.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

import sendgrid
from sendgrid import Mail, SendGridClient
from sendgrid import SendGridError, SendGridClientError, SendGridServerError

celery = Celery('tasks', broker=settings.redis_broker)

# sendgrid client
sg = sendgrid.SendGridClient(settings.sg_user, settings.sg_key, raise_errors=True)

@celery.task(ignore_result=True)
def sendMail(to, mail, username):
    logging.basicConfig(filename='SendMail.log', level=logging.DEBUG)
    try:
        to_send = "http://taskwetu.heroku.com/confirm/" + str(username) + "/" + str(mail) + "/"

        message = sendgrid.Mail()
        message.add_to(to)
        message.set_subject('Taskwetu Sign-Up Confirmation')
        message.set_html("<p>" + to_send + "</p>")
        message.set_text( str(to_send) )
        message.set_from('taskwetu <taskkwetu@gmail.com>')

        # status, msg = sg.send(message)
        sg.send(message)

    except SendGridClientError as e:
        logging.warning('Mail failed Client Error %s' % str(e))
    except SendGridServerError as e:
        logging.warning('Mail failed Server Error %s' % str(e))


@celery.task(ignore_result=True)
def new_task_message(to, mail, username):
    logging.basicConfig(filename='SendMail.log', level=logging.DEBUG)
    try:
        to_send = "New Task has been created by user %s" %(username)
        logo = '<img src="http://188.226.195.158/static/ico/taskwetu_logo.png"/>'

        html = "<h3> %s </h3><br><p> %s </p>" %(logo, to_send)

        message = sendgrid.Mail()
        message.add_to(to)
        message.set_subject('New Task Created')
        message.set_html(html)
        message.set_text( str(to_send) )
        message.set_from('TaskWetu <taskkwetu@gmail.com>')

        # status, msg = sg.send(message)
        sg.send(message)

    except SendGridClientError as e:
        logging.warning('Mail failed Client Error %s' % str(e))
    except SendGridServerError as e:
        logging.warning('Mail failed Server Error %s' % str(e))


@celery.task(ignore_result=True)
def passwordReset(to, newpassword):
    try:
        to_send = "http://taskwetu.heroku.com/"

        message = sendgrid.Mail()
        message.add_to(to)
        message.set_subject('Taskwetu Password Reset')
        message.set_html("<p>" + to_send + "</p>" +  "<p>" + newpassword + "</p>")
        message.set_text( str(to_send) )
        message.set_from('taskwetu <taskkwetu@gmail.com>')

        sg.send(message)

    except SendGridClientError as e:
        logging.warning('Mail failed Client Error %s' % str(e))
    except SendGridServerError as e:
        logging.warning('Mail failed Server Error %s' % str(e))


@celery.task(ignore_result=True)
def sendText(to, code):
    logging.basicConfig(filename='SMS.log', level=logging.DEBUG)

    gateway = AfricasTalkingGateway(settings.username, settings.apikey)
    message = "Welcome to taskwetu, an errand running platform. Your User Code is %s " % (code)

    recipients = gateway.sendMessage(to, message)

    try:
        for recipient in recipients:
            logging.info('number=%s;status=%s;messageId=%s;cost=%s'
                         % (recipient['number'], recipient['status'],
                            recipient['messageId'], recipient['cost']))

    except AfricasTalkingGatewayException, e:
        logging.warning('Database setup completed %s' % str(e))


@celery.task(ignore_result=True)
def send_notification_task(to, taskData):
    logging.basicConfig(filename='SMS.log', level=logging.DEBUG)

    gateway = AfricasTalkingGateway(settings.username, settings.apikey)
    message = "New Task Has been created %s " % (taskData)
    recipients = gateway.sendMessage(to, message)

    try:
        for recipient in recipients:
            logging.info('number=%s;status=%s;messageId=%s;cost=%s'
                         % (recipient['number'], recipient['status'],
                            recipient['messageId'], recipient['cost']))

    except AfricasTalkingGatewayException, e:
        logging.warning('SMS failed to send %s' % str(e))


def dbSetup():
    connection = r.connect(host=settings.RDB_HOST, port=settings.RDB_PORT, auth_key=settings.rethinkdb_auth)
    try:
        r.db_create(settings.LINK_DB).run(connection)
        r.db(settings.LINK_DB).table_create('User').run(connection)
        logging.info('Database setup completed')
    except RqlRuntimeError:
        logging.info('App database already exists')
    finally:
        connection.close()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in request.cookies:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def before_request():
    try:
        if 'username' not in request.cookies:
            redirect('/')

        logging.info('before_request')
        g.rdb_conn = r.connect(host=settings.RDB_HOST, port=settings.RDB_PORT, db=settings.LINK_DB, auth_key=settings.rethinkdb_auth)
    except RqlDriverError:
        """
        log_data = "LOG_INFO=" + simplejson.dumps({ 'Request':'app.before failed database' })
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
