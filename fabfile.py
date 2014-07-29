from fabric.api import *

env.user = 'root'
env.hosts = ['188.226.195.158']


def setup_server():
    run('mkdir /tmp/TaskWetu')
    with cd('/tmp/TaskWetu'):
        run('git clone https://github.com/nailab/linkus.git')
        with cd('linkus'):
            run('pip install -r requirements.txt')
            run('gunicorn -c config-gunicorn.py app:app')
            prepare_deploy()


def clean():
    run('rmdir /tmp/TaskWetu')
    run('rmdir /tmp/TaskWetu/linkus')
    run('apt-get clean && apt-get dist-upgrade')
    local('echo cleaning ...')


def installDeps():
    pass


def prepare_deploy():
    run("apt-get update && apt-get -y dist-upgrade")


def restartNginx():
    run('service nginx restart')


def deploy():
    prepare_deploy()
    setup_server()
    restartNginx()
