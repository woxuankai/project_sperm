#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import daemon
import lockfile
import signal
import os
import os.path
import time
import logging
import errno
from main_job import main_job

#time waiting for a process to terminate after send sigterm
term_wait = 0.5
term_wait_repeat = 20


# for daemon.open()
# will ovewrite it if the specified pid file already exits
class _pidfile:
    def __enter__(self):
        with open(self.path,'w') as f:
            print(os.getpid(),file=f)
        self._is_open = True
        return
    def __exit__(self,exc_type, exc_val, exc_tb):
        self._is_open = False
        pass
    def __init__(self, pidfile_path):
        self._is_open = False
        self.path = pidfile_path



# return when daemonized
# exit when error occur
# for todo=start, main_init and daemonize main_do
# for todo=stop, send signal_term to the main_do
# for todo=restart, stop and then start

def entry(config,todo):
    config_basic = config.get('basic',{'name':'default'})
    loggername = config_basic.get('name','default')
    loggername = 'entry.' + loggername
    logger = logging.getLogger(loggername)
    def entry_start(config):
        # parse config file
        try:
            config_daemon=config['daemon']
            context = daemon.DaemonContext()
            context.working_directory = \
                config_daemon.get('working_directory','/')
            context.umask = config_daemon.get('umask', 0o000)
            #must specify one for sig_term
            context.pidfile = _pidfile(config_daemon['pidfile'])
            context.uid = config_daemon.get('uid', os.getuid())
            context.gid = config_daemon.get('gid', os.getgid())
            if 'stdin' in config_daemon:
                f = open(config_daemon['stdin'],'r')
                context.stdin = f
            if 'stdout' in config_daemon:
                f = open(config_daemon['stdout'],'a')
                context.stdout = f
            if 'stderr' in config_daemon:
                if ('stdout' not in config_daemon) \
                   or (config_daemon['stdout'] != config_daemon['stderr']):
                    # in prevention of open the same file twice
                    f = open(config_daemon['stderr'],'a')
                context.stderr = f
            #context.signal_map = {signal.SIGTERM : main_clean}
            #use default map
            #main_clean has to receive 'config', to be completed in ohter way
        except Exception:
            logger.exception('failed to set daemon context')
            sys.exit(1)
        logger.info('daemon context inited')

        try:
            pid = os.fork()
            assert pid >= 0
        except:
            logger.exception('failed to fork')
            sys.exit(1)
        if pid > 0:
            logger.info('forked, the child process is expected to daemonize')
            #parent return
            return
        #child init and daemonize
        try:
            with context:
                do_it = main_job(config)
                with do_it:
                    pass
        except Exception as e:
            if (type(e) != SystemExit) or (e.code != 0):
                logger.exception(\
                    'something wrong with child or grandchild')
            else:
                logger.info('exited with 0')
            return
        sys.exit(1)

            
    def entry_stop(config):
        #send sig_term and wait some time
        try:
            pidfile = config['daemon']['pidfile']
        except:
            logger.exception('no pidfile specified')
            sys.exit(1)
        if not os.path.exists(pidfile):
            logger.warning('not running (no such pid file')
            return
        # the pid file exitsn
        try:
            with open(pidfile,'r') as f:
                pid = f.read()
                pid = int(pid)
                assert pid > 0
        except:
            logger.exception('error getting pid from pidfile')
            sys.exit(1)
        try:
            os.kill(pid, signal.SIGTERM)
        except Exception as e:
            if type(e) == OSError and e.errno == errno.ESRCH:
                logger.info('pid not running')
                return
            else:
                logger.exception('failed to kill {}'.format(pid))
                sys.exit(1)
        for cnt in range(0,term_wait_repeat):
            time.sleep(term_wait)
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError as e:
                if e.errno == errno.ESRCH:
                    logger.info('terminated')
                    # the parent will exit, so don't have to wait()
                    return
        logger.error('time out wait for terminating')
        sys.exit(1)
    
    
    if todo=='start':
        entry_start(config)
    elif todo=='stop':
        entry_stop(config)
    elif todo=='restart':
        entry_stop(config)
        entry_start(config)
    else:
        logger.error('unkown todo')
        #raise AttributeError('start|stop|restart')
        sys.exit(1)
    return
