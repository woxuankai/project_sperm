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
from main_job import main_do, main_clean, main_init

#time waiting for a process to terminate after send sigterm
term_wait = 0.5
term_wait_repeat = 20


# for daemon.open()
# will ovewrite it if the specified pid file already exits
class _pidfile:
    def __enter__(self):
        with open(self.path,'w') as f:
            print(os.getpid(),file=f)
        return
    def __exit__(self,exc_type, exc_val, exc_tb):
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
        except Exception:
            logging.exception('failed to set daemon context')
            sys.exit(1)

        context.signal_map = {
            signal.SIGTERM : main_clean}
        logging.info('daemon context inited')
        try:
            pid = os.fork()
            assert pid != -1
        except:
            logging.exception('failed to fork')
            sys.exit(1)
        if pid > 0:
            logging.info('forked, the child process is expected to daemonize')
            #parent return
            return
        #child init and daemonize
        try:
            main_init(config)
            with context:
                main_do(config)
        except Exception as e:
            logging.info('#############################')
            if (type(e) == SystemExit) or (e.code != 0):
                logging.exception(\
                    'something wrong with child or grandchild')
            else:
                logging.info('exited with 0')
        sys.exit(1)

            
    def entry_stop(config):
        #send sig_term and wait some time
        try:
            pidfile = config['daemon']['pidfile']
        except:
            logging.exception('no pidfile specified')
            sys.exit(1)
        if not os.path.exists(pidfile):
            logging.warning('not running (no such pid file')
            return
        # the pid file exitsn
        try:
            with open(pidfile,'r') as f:
                pid = f.read()
                pid = int(pid)
                assert pid > 0
        except:
            logging.exception('error getting pid from pidfile')
            sys.exit(1)
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            if e.errno == errno.ESRCH:
                logging.info('pid not running')
            else:
                logging.exception('failed to send signal {}'.format(pid))
                sys.exit(1)
        for cnt in range(0,term_wait_repeat):
            time.sleep(time_term)
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError as e:
                if e.errono == errno.ESRCH:
                    logging.info('terminated')
                    return
        logging.error('time out wait for terminating')
        sys.exit(1)
        return
    
    
    if todo=='start':
        entry_start(config)
    elif todo=='stop':
        entry_stop(config)
    elif todo=='restart':
        entry_stop(config)
        entry_start(config)
    else:
        logging.error('unkown todo')
