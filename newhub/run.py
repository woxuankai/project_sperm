#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
import os
import os.path
from getconfig import getconfig
from daemon import daemon_start
if __name__ == '__main__':
    # slove path problems
    logging.basicConfig(level=logging.DEBUG)
    try:
        node2start = sys.argv.copy()
        if len(node2start) < 4:
            raise NameError("not enough arguments")
        # argument 0 - path of run.py
        basedir = os.path.dirname(node2start.pop(0))
        # add mods folder to path
        basedir = os.path.abspath(basedir)
        modpath = os.path.join(basedir, "./mods")
        assert(os.path.isdir(modpath))
        sys.path.append(modpath)
        # argument 1 - path of config file
        configfilepath = os.path.abspath(node2start.pop(0))
        if not os.path.isfile(configfilepath):
            raise NameError("not a config file")
        # argument 2 - what to do? start|stop|restart
        todo = node2start.pop(0)  # under development
        # argument 3:end - nodes to run
        # the reset of sys.argv(node2start)

    except Exception:
        logging.exception("\
usage: run.py configfile start|stop|restart node1 node2 node3...")
        exit(1)
    # load config file
    try:
        config = getconfig(configfilepath)
    except Exception:
        logging.exception('fail to load config file: ' + configfilepath)
        exit(1)
    for nodename in node2start:
        logging.info('try to start node <{}>'.format(nodename))
        try:
            nodeconfig = config[nodename].copy()
        except:
            logging.exception(
                'no item in configfile for node <{}>'.format(nodename))
            continue
        nodeconfig['nodename'] = nodename
        try:
            daemon_start(nodeconfig)
        except Exception:
            logging.exception(
                'failed to start node daemon<{}>'.format(nodename))
        else:
            logging.info('node daemon <{}> started'.format(nodename))
    logging.info('all nodes started, exit now')
    exit(0)
