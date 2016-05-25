#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parsedata(data):
    return float(data[6:14].replace(' ',''))

from postdata import postdata
def uploaddata(data, nodeinfo):
    weight = parsedata(data)
    res = postdata(nodeinfo['srvaddr'], nodeinfo['id'] , weight)
