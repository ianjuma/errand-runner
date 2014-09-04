import os

# flask app
DEBUG=False
SECRET_KEY="I\xf9\x9cF\x1e\x04\xe6\xfaF\x8f\xe6)-\xa432"
CSRF_ENABLED=True
CSRF_SESSION_LKEY='dev_key_h8asSNJ9s9=+'
THREADED = False
ONLINE_LAST_MINUTES = 720

salt = 'd40037e1ff7841838235533d910bbf24'

# sms API key
username = "IanJuma"
apikey = "840a1b44b95cb68ab856cab41237700266dc22e5a795e341c067a02cbc3cb937"

# sendgrid key
sg_user = "app27418636@heroku.com"
sg_key = "w4do409h"

# redis broker
redis_broker = "redis://localhost:6379/0"
rabbit_mq    = "amqp://localhost:5672//"

# rethink pass
rethinkdb_auth = "taskwetu_db**//"
RDB_HOST = os.environ.get('RDB_HOST') or '127.0.0.1'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
LINK_DB = 'LinkUs'

# celery
C_FORCE_ROOT="True"
