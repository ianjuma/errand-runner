from fabric.api import *

env.user = 'root'
env.hosts = ['188.226.195.158']


def setup_server():
    run('mkdir /tmp/TaskWetu')
    with cd('tmp/TaskWetu'):
        run('pip install -r requirements.txt')
        prepare_deploy()
        deploy()
        run('gunicorn -c config-gunicorn.py app:app')


def prepare_deploy():
	app_dir = '/tmp/TaskWetu/'
    local("apt-get update && apt-get -y dist-upgrade")


def restartNginx():
    sudo('service nginx restart')


def deploy():
    run('gunicorn -c config-gunicorn.py app:app')
