#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import importlib
import sys

def initlogger(config_basic):
    leveldict = {
        'CRITICAL' : logging.CRITICAL,
        'ERROR'    : logging.ERROR,
        'WARNING'  : logging.WARNING,
        'INFO'     : logging.INFO,
        'DEBUG'    : logging.DEBUG,
        'NOTSET'   : logging.NOTSET}
    #as only root logger is used, we discard logger name
    defaultlogformat = '%(asctime)s - %(levelname)s : %(message)s'
    #defaultlogformat = '%(asctime)s - %(levelname)s - %(name)s : %(message)s'
    # only root logger writes to logfile
    logging.basicConfig(
        filename = config_basic['filename'], # must specify one
        level    = config_basic.get('level','WARNING'),
        format   = config_basic.get('format',defaultlogformat))
    #logger = logging.getLogger(configbasic.get('name','defaultname'))
    #logger = logging.getLogger()
    #logger.info('logger init finished')
    #return logger


def main_clean(config):
    pass

#clean and init logger
def main_init(config):
    initlogger(config['basic'])
    main_clean(config)

    # the main job to do
def main_do(config):
    logger = logging.getLogger()
    try:
        start_delay   = config['basic']['start_dealy']
        repeat_time   = config['basic']['repeat_time']
        restart_delay = config['basic']['restart_delay']
        nodeconfig    = config['spec']
    except:
        logger.exception('failed to parse config')
        sys.exit(1)
    try:
        mod = importlib.import_module("mod_" + config['basic']['nodetype'])
        handler_run = getattr(mod, "run")
        handler_fix = getattr(mod, "fix")
    except:
        logger.exception('failed to load mod or func')
        sys.exit(1)
    logger.info('ready to start')
    #   wait a moment
    try:
        time.sleep(start_delay)
    except:
        logger.exception('failed to do start delay')
        sys.exit(1)
    logger.info('now fork for work process')
    #   fork for work process
    cnt = 0
    while cnt < repeat_time or repeat_time < 0:
        cnt = cnt + 1
        # fork for work func
        try:
            pid = os.fork()
            assert pid >= 0
        except:
            logger.exception('failed to fork for work func')
        # the child process
        if pid == 0:
            logger.info('forked for work func')
            handler_run(nodeconfig, logger, cnt)
            logger.warning('work func return')
            sys.exit(0)

        # parent process
        pid, status = os.wait()
        exitcode = int(status >> 8)
        if exitcode == 0:
            logger.warning('return code {}'.format(exitcode))
        logger.info('work process exited with {}'.format(exitcode))

        logger.info('#{}: wait and restart worker'.format(cnt))
        try:
            time.sleep(restart_delay)
        except:
            logger.exception('failed to do restart delay')
            break
    # end of while
    logger.info('exit daemon process now')
    exit(0)


#import sys
#import os
#import os.path
#if __name__ == '__main__':
#    modpath = os.path.abspath(sys.argv[0])
#    modpath = os.path.dirname(modpath)
#    modpath = os.path.join(modpath, "./mods")
#    sys.path.append(modpath)
#    nodeconfig = {"nodetype": "test",
#                  "start_delay": 2,
#                  "restart_delay": 2,
#                  "repeat_time": 5,
#                  "logpath": "./__pycache__/",
#                  "logformat": "%(asctime)s - %(levelname)s - %(name)s : %(message)s",
#                  "pidfile": "/temp/project_sperm_test0.pid",
#                  "dpidfile": "/temp/project_sperm_test0d.pid",
#                  "stdout": "/dev/null",
#                  "stdin": "/dev/null",
#                  "stderr": "/dev/null",
#\
#                  "exitcode": 1, "fixexitcode": 0}
#    nodeconfig['nodename'] = 'test0'
#    daemon_start(nodeconfig)
#
#   "test0":
#   {
#       "nodetype":"test",
#       "start_delay":5,
#       "restart_delay":5,
#       "repeat_time":5,
#       "logpath":"/var/log/project_sperm/",
#       "logformat":"%(asctime)s - %(levelname)s - %(name)s : %(message)s",
#       "pidfile":"/temp/project_sperm_test0.pid",
#       "dpidfile":"/temp/project_sperm_test0d.pid",
#       "stdout":"/dev/null",
#       "stdin":"/dev/null",
#       "stderr":"/dev/null",
#
#       "exitcode":0
#   }
#
#
#
#
#            # fork for fix func
#            try:
#                pid = os.fork()
#            except:
#                logger.exception('failed to fork to fix problems')
#            if pid == 0:
#                # child
#                handler_fix(nodeconfig, logger, exitcode)
#                logger.warning('fix func return')
#                exit(0)
#            # parent
#            pid, status = os.wait()
#            exitcode = int(status >> 8)
#            logger.info('fix process exited with {}'.format(exitcode))
#            if exitcode != 0:
#                # failed to fix problem
#                logger.error('failed to fix problems')
#                break
#            else:
#                logger.info('successfully fixed problems')
#
