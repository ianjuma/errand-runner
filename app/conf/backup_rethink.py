#! /usr/bin/env python

import os
from subprocess import call


def check_dir_exist(os_dir):
    if not os.path.exists(os_dir):
        exit(1)


def backup():
    check_dir_exist('/root/rethink_backup/')
    os.chdir('/root/rethink_backup/')
    call(["rethinkdb-dump", "-a", "taskwetu_db**//"])

if __name__ == '__main__':
    backup()
