#! /usr/bin/env python

import sendgrid

from sendgrid import Mail, SendGridClient
from sendgrid import SendGridError, SendGridClientError, SendGridServerError

import logging
logging.basicConfig(filename='SendMail.log', level=logging.DEBUG)

sg = sendgrid.SendGridClient('app27418636@heroku.com', 'w4do409h', raise_errors=True)


def sendMail(to, mail, username):
    try:
        to_send = "http://taskwetu.heroku.com/confirm/" + str(username) + "/" + str(mail) + "/"

        message = sendgrid.Mail()
        message.add_to(to)
        message.set_subject('Taskwetu Sign-Up Confirmation')
        message.set_html("<p>" + to_send + "</p>")
        message.set_text( str(to_send) )
        message.set_from('LinkUs <taskkwetu@gmail.com>')

        # status, msg = sg.send(message)
        sg.send(message)

    except SendGridClientError as e:
        logging.warning('Mail failed Client Error %s' % str(e))
    except SendGridServerError as e:
        logging.warning('Mail failed Server Error %s' % str(e))


def passwordReset(to, newpassword):
    try:
        to_send = "http://taskwetu.heroku.com/"

        message = sendgrid.Mail()
        message.add_to(to)
        message.set_subject('Taskwetu Password Reset')
        message.set_html("<p> Your new Password: " + to_send + "</p>" +  
            "<p>" + newpassword + " Please keep this a secret</p>")
        message.set_text( str(to_send) )
        message.set_from('taskwetu <taskkwetu@gmail.com>')

        sg.send(message)

    except SendGridClientError as e:
        logging.warning('Mail failed Client Error %s' % str(e))
    except SendGridServerError as e:
        logging.warning('Mail failed Server Error %s' % str(e))