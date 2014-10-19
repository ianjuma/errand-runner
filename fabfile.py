from fabric.api import *

env.user = 'root'
env.hosts = ['188.226.195.158']


def moveSupervisor():
    run('mv /tmp/TaskWetu/taskwetu/supervisord.conf /etc/supervisord.conf')


def setSupervisordLog():
    run('mkdir /var/log/supervisord/')


def startCelery():
    run('celery -A app.celery worker --loglevel=INFO --concurrency=10')


def supervisor():
    run('kill -9 `pgrep gunicorn`')
    run('kill -9 `pgrep supervisor`')
    run('kill -9 `pgrep celery`')
    run('export C_FORCE_ROOT="true"')
    run('supervisord -c /etc/supervisord.conf')


def setup_server(version):
    run('pty=False')
    with cd('/tmp/TaskWetu'):
        # run('git clone https://github.com/nailab/taskwetu.git')
        with cd('/tmp/TaskWetu/taskwetu'):
            # run('git checkout tags/%s' % (version,))
            result = run('pip install -r requirements.txt')
            if result.failed:
                local('GUNICORN failed')

            #prepare_deploy()


def backUp():
    run('rethinkdb-dump -a taskwetu_db**//')


def installDeps():
    run('apt-get install redis')
    run('apt-get install rabbitmq-server')
    run('apt-get install rethinkdb')


def mvStatic():
    run('rm -rf /www/data/static')
    run('mv /tmp/TaskWetu/taskwetu/app/static /www/data/')


def prepare_deploy():
    run("apt-get update && apt-get -y dist-upgrade")
    run('apt-get clean && apt-get autoremove --purge --assume-yes')


def restartNginx():
    run('service nginx restart')


def deploy(version="0.6.0"):
    setup_server(version)
    mvStatic()
    supervisor()
    restartNginx()
