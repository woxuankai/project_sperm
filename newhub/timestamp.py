#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
ISOTIMEFORMAT='%Y-%m-%d %X'
#display timestamp
def disptimestamp():
	stimenow = time.strftime( ISOTIMEFORMAT, time.gmtime() )
	print('UTC:',stimenow)

if __name__ == '__main__':
	disptimestamp()
