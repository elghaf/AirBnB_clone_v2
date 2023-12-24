#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 08 14:21:54 2023
@author: Etinosa Noma-Osaghae
"""
from fabric.api import local, put, run, env, cd, lcd
from datetime import datetime
import os


env.hosts = ['54.237.76.209', '35.175.63.185']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """
    Compress webstatic folder before deploying
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    local('sudo mkdir -p ./versions')
    path = './versions/web_static_{}'.format(now)
    local('sudo tar -czvf {}.tgz web_static'.format(path))
    name = '{}.tgz'.format(path)
    if name:
        return name
    else:
        return None


def do_deploy(archive_path):
    """Deploy the compressed webstatic folder to webservers
    """
    try:
        archive = archive_path.split('/')[-1]
        path = '/data/web_static/releases/' + archive.strip('.tgz')
        current = '/data/web_static/current'
        put(archive_path, '/tmp')
        run('mkdir -p {}'.format(path))
        run('tar -xzf /tmp/{} -C {}'.format(archive, path))
        run('rm /tmp/{}'.format(archive))
        run('mv {}/web_static/* {}'.format(path, path))
        run('rm -rf {}/web_static'.format(path))
        run('rm -rf {}'.format(current))
        run('ln -s {} {}'.format(path, current))
        print('New version deployed!')
        return True
    except:
        return False


def deploy():
    """
    This function is used to deploy pages to webservers
    """
    archive_path = do_pack()
    answer = do_deploy(archive_path)
    return answer


def gets_out_of_date(number, _type):
    """This function gets some old versions of files in webserver
    """

    if number == 0:
        number = 1

    if _type == 'local':
        content = local("ls -td web_static_*", capture=True)
    elif _type == 'remote':
        content = run("ls -td web_static_*")

    content_list = content.split()
    out_of_date = content_list[number:]
    return out_of_date


def do_clean(number=0):
    """This function helps to delete older versions of files
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
