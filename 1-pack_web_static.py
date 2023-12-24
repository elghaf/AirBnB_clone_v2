#!/usr/bin/python3
from fabric.api import local
from datetime import date
from time import strftime


def do_pack():
    """ This script generates an archive of the webstatic folder"""

    filename = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(filename))

        return "versions/web_static_{}.tgz".format(filename)

    except Exception as e:
        return None
