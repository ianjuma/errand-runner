import os

secret = os.urandom(24)


DEBUG=False
SECRET_KEY=""
CSRF_ENABLED=True
CSRF_SESSION_LKEY='dev_key_h8asSNJ9s9=+'
THREADED = False

# sms API key
username = "IanJuma"
apikey = "840a1b44b95cb68ab856cab41237700266dc22e5a795e341c067a02cbc3cb937"

# sendgrid key
sg_user = "app27418636@heroku.com"
sg_key = "w4do409h"

# redis broker
redis_broker='redis://localhost:6379/0'