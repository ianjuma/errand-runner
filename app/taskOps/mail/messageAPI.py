from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

import logging
logging.basicConfig(filename='SMS.log', level=logging.DEBUG)

username = "IanJuma"
apikey = "840a1b44b95cb68ab856cab41237700266dc22e5a795e341c067a02cbc3cb937"
# Please ensure you include the country code (+254 for Kenya in this case)


class Validate():
    """
    Format mobile number - add country code
    """

    def __init__(mobileNo):
        mobileNo = mobileNo

    def validate(mobileNo):
        """
        validate func(mobileNo) -> mobileNo
        """
        mobileNo = str(mobileNo)

        if mobileNo.startswith('0'):
            mobileNo = mobileNo[1:]

        mobileNo = "+254"+mobileNo
        return mobileNo


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