#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 14:21:54 2023
@author: Etinosa Noma-Osaghae
"""
from fabric.api import local, put, run, env
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['54.237.76.209', '35.175.63.185']


def do_pack():
    """Create a .tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """This function distributes the archive to webservers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False


def deploy():
    """This function creates and distributes an archive to webservers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
