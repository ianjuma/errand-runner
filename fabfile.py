from fabric.api import *

env.user = 'root'
env.hosts = ['188.226.195.158']


def setup_server():
    run('mkdir /tmp/TaskWetu')
    with cd('/tmp/TaskWetu'):
        run('git clone https://github.com/nailab/linkus.git')
        with cd('/tmp/TaskWetu/linkus'):
            run('pip install -r requirements.txt && gunicorn -c config-gunicorn.py app:app')
            run('gunicorn -c config-gunicorn.py app:app')
            prepare_deploy()


def clean():
    run('rm -r /tmp/TaskWetu')
    run('rm -r /tmp/TaskWetu/linkus')
    run('apt-get clean && apt-get dist-upgrade')
    local('server cleaned up ...')


def installDeps():
    run('apt-get install redis')
    run('apt-get install postgresql9.3')
    run('apt-get install rethinkdb')


def prepare_deploy():
    run("apt-get update && apt-get -y dist-upgrade")


def restartNginx():
    run('service nginx restart')


def deploy():
    prepare_deploy()
    setup_server()
    restartNginx()
