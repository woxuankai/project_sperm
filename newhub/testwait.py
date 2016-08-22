#!/bin/python3

import os,time

if __name__ == "__main__":
    time.sleep(3)
    print('#1 fork')
    pid1 = os.fork()
    if pid1 == 0:
        #the child process
        time.sleep(3)
        print('#2 fork')
        pid2 = os.fork()
        if pid2 == 0:
            #the grandson process
            time.sleep(1)
        else:
            #the child process
            print('the grandson process pid {}'.format(pid2))
            time.sleep(3)
            print('the child process is waiting')
            pid, status = os.wait()
            print('the child process waited pid {}'.format(pid))
    else:
        # the parent process
        print('the child process pid {}'.format(pid1))
        print('the parent process is waiting')
        pid, status = os.wait()
        print('the parent process waited pid {}'.format(pid))
    exit(0)

#--------------------------------------------
#conclusion
#the wait() function
#will wait for his own child process but not grandson process
