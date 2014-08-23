from celery import Celery
from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

import logging
logging.basicConfig(filename='SMS.log', level=logging.DEBUG)

username = "IanJuma"
apikey = "840a1b44b95cb68ab856cab41237700266dc22e5a795e341c067a02cbc3cb937"

app = Celery('tasks', backend='amqp', broker='amqp://')

@app.task(ignore_result=True)
def sendText(to, code):
    gateway = AfricasTalkingGateway(username, apikey)
    message = "Welcome to LinkUs, an errand running platform. Your User Code is %s " % (code)

    recipients = gateway.sendMessage(to, message)

    try:
        for recipient in recipients:
            logging.info('number=%s;status=%s;messageId=%s;cost=%s'
                         % (recipient['number'], recipient['status'],
                            recipient['messageId'], recipient['cost']))

    except AfricasTalkingGatewayException, e:
        logging.warning('Database setup completed %s' % str(e))


@app.task(ignore_result=True)
def send_notification_task(to, taskData):
    gateway = AfricasTalkingGateway(username, apikey)
    message = "New Task Has been created %s " % (taskData)
    recipients = gateway.sendMessage(to, message)

    try:
        for recipient in recipients:
            logging.info('number=%s;status=%s;messageId=%s;cost=%s'
                         % (recipient['number'], recipient['status'],
                            recipient['messageId'], recipient['cost']))

    except AfricasTalkingGatewayException, e:
        logging.warning('SMS failed to send %s' % str(e))