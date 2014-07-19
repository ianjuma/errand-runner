#! /usr/bin/env python

import sendgrid

from sendgrid import Mail, SendGridClient
from sendgrid import SendGridError, SendGridClientError, SendGridServerError

import logging
logging.basicConfig(filename='SendMail.log', level=logging.DEBUG)

sg = sendgrid.SendGridClient('app27418636@heroku.com', 'w4do409h', raise_errors=True)


def sendMail(to, mail, username):
    try:
        message = sendgrid.Mail()
        message.add_to(to)
        message.set_subject('LinkUs')
        message.set_html('Body')
        message.set_text(mail)
        message.set_from('LinkUs <linkus@gmail.com>')

        # status, msg = sg.send(message)
        sg.send(message)

    except SendGridClientError as e:
        logging.warning('Mail failed Client Error %s' % str(e))
    except SendGridServerError as e:
        logging.warning('Mail failed Server Error %s' % str(e))



sendMail("wjuma@students.usiu.ac.ke", "ALL", "IanJuma")