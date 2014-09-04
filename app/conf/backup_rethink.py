#! /usr/bin/env python

import os


def check_dir_exist(os_dir):
    if not os.path.exists(os_dir):
        exit(1)


def backup():
    check_dir_exist('/root/rethink_backup/')
    with  os.chdir('/root/rethink_backup/'):
        args = ("-a", "taskwetu_db**//")
        os.execl("/usr/local/bin/rethinkdb-dump", args)

if __name__ == '__main__':
    backup()
