#! /usr/bin/env python

import sendgrid

from sendgrid import Mail, SendGridClient
from sendgrid import SendGridError, SendGridClientError, SendGridServerError

from celery import Celery
app = Celery('tasks', backend='amqp', broker='amqp://')

import logging
logging.basicConfig(filename='SendMail.log', level=logging.DEBUG)

sg = sendgrid.SendGridClient('app27418636@heroku.com', 'w4do409h', raise_errors=True)


@app.task(ignore_result=True)
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