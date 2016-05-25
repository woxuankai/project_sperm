#!/usr/bin/env python3
# -*- coding: utf-8 -*-

configfilepath = './config.json'

import os, time
from getnodes import getnodes
from startnode import startnode
if __name__ == '__main__':
    print('program start!')
    #get nodes info
    try:
        nodes=getnodes(configfilepath);
    except Exception as e:
        print('fail to  parse file: ',configfilepath)
        print('details: ',e)
    #one node, one process
    childpids = {};
    while len(nodes) >= 1:
        nodename,nodeinfo = nodes.popitem()
        pid = os.fork()
        if pid == 0:
            #child process
            try:
                nodeinfo['nodename'] = nodename
                startnode(nodeinfo)
            except Exception as e:
                print('failed to start node: {}'.format(nodename))
                print('details: ',e)
                exit(-1)
            #shouldn't reach here
            exit(0)
        else:
            #parent process
            childpids[pid]=nodename
            time.sleep(0.5)
            #continue to fork
    #forked one process per node
    #wait for every process to finish
    while len(childpids) >= 1:
        pid,status = os.wait()
        exitchildname = childpids.pop(pid);
        print('process for node <{}> exited'.format(exitchildname))
        print('exit status indication: ',status)
    #child processes should never return
    #thus program shouldn't come here
    exit(0)
