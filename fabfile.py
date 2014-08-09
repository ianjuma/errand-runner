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


def moveStatic():
    with cd('/tmp/TaskWetu/linkus/app/'):
        run('mv static ')


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

            prepare_deploy()


def clean():
    run('rm -r /tmp/TaskWetu')
    run('apt-get clean && apt-get autoremove -y')


def installDeps():
    run('apt-get install redis')
    run('apt-get install postgresql9.3')
    run('apt-get install rethinkdb')


def prepare_deploy():
    run("apt-get update && apt-get -y dist-upgrade")


def restartNginx():
    run('service nginx restart')


def deploy(version="v0.1.3"):
    setup_server(version)
    moveSupervisor()
    supervisor()
    restartNginx()
