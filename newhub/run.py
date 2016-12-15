#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
import os
import os.path
from getconfig import getconfig
from entry import entry

mods_dir='./mods'

if __name__ == '__main__':
    # slove path problems
    # no need to redirect output to stdout instead stderr
    # because stderr can also be redirected to a file
    # logging.basicConfig(level=logging.DEBUG,\
    #                     stream=logging.StreamHandler(sys.stdout))
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('root')
    logger.info('#########################################')
    logger.info('############# WELCOME !!!!!!! ###########')
    logger.info('#########################################')
    try:
        node2start = sys.argv.copy()
        if len(node2start) < 3:
            raise NameError("not enough arguments")
        # argument 0 - path of run.py
        basedir = os.path.dirname(node2start.pop(0))
        # add mods folder to path
        basedir = os.path.abspath(basedir)
        modpath = os.path.join(basedir, mods_dir)
        assert(os.path.isdir(modpath))
        sys.path.append(modpath)
        # argument 1 - path of config file
        configfilepath = os.path.abspath(node2start.pop(0))
        if not os.path.isfile(configfilepath):
            raise NameError("not a config file")
        # argument 2 - what to do? start|stop|restart
        todo = node2start.pop(0)  # under development
    except Exception:
        logger.exception("\
usage: run.py configfile start|stop|restart")
        exit(1)

    # load config file
    logger.info('loading config file...')
    try:
        config = getconfig(configfilepath)
        config_basic = config['basic'].copy()
        config_daemon = config['daemon'].copy()
        config_spec = config['spec'].copy()
    except Exception:
        logger.exception('fail to load config file: ' + configfilepath)
        exit(1)
    logger.info('passing arguments to entry...')
    try:
        entry(config,todo)
    except Exception:
        logger.exception('failed to start entry')
        exit(1)
    logger.info('returned from entry, exit now')
    logger.info('################  end  ##################')
    exit(0)
