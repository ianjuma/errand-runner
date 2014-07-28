def setup_server():


def prepare_deploy():
	app_dir = '/root/TaskWetu/'
    local("apt-get update && apt-get dist-upgrade -y")
    local("")