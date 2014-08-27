from fabric.api import *

env.user = 'root'
env.hosts = ['188.226.195.158']


def moveSupervisor():
    run('mv /tmp/TaskWetu/linkus/supervisord.conf /etc/supervisord.conf')
    with cd('/tmp/TaskWetu/linkus'):
        put('supervisord.conf')


def setSupervisordLog():
    run('mkdir /var/log/supervisord/')


def supervisor():
    run('supervisord -c /etc/supervisord.conf')


def setup_server(version):
    run('pty=False')
    run('mkdir /tmp/TaskWetu')
    with cd('/tmp/TaskWetu'):
        run('git clone https://github.com/nailab/linkus.git')
        with cd('/tmp/TaskWetu/linkus'):
            run('git checkout tags/%s' % (version,))
            result = run('pip install -r requirements.txt')
            if result.failed:
                local('GUNICORN failed')

            #prepare_deploy()


def clean():
    run('rm -r /tmp/TaskWetu')


def backUp():
    run('rethinkdb-dump')


def installDeps():
    run('apt-get install redis')
    run('apt-get install rabbitmq-server')
    run('apt-get install rethinkdb')


def mvStatic():
    run('rm -rf /www/data/static')
    run('mv /tmp/TaskWetu/linkus/app/static /www/data/')


def prepare_deploy():
    run("apt-get update && apt-get -y dist-upgrade")
    run('apt-get clean && apt-get autoremove --purge --assume-yes')


def restartNginx():
    run('service nginx restart')


def deploy(version):
    setup_server(version)
    moveSupervisor()
    mvStatic()
    supervisor()
    restartNginx()
