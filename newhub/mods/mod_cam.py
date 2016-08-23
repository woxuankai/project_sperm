#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pygame.camera
from urllib import request, parse
import json


def caponeframe(imgpath, dev, resolution):
    pygame.camera.init()
    cam = pygame.camera.Camera(dev, resolution)
    cam.start()
    img = cam.get_image()
    cam.stop()
    pygame.image.save(img, imgpath)
    return 0


def uploadoneframe(serveraddr, imgpath):
    imgfile = open(imgpath, 'rb')
    #reqdata = parse.urlencode([('image', imgfile.read())])
    reqdata = imgfile.read()
    imgfile.close()
    req = request.Request(serveraddr)
    # with request.urlopen(req, data = reqdata.encode('utf-8')) as f:
    with request.urlopen(req, data=reqdata) as f:
        if f.status >= 400:
            raise ConnectionError('HTTP ERR: ', f.status)
        res = f.read()
        #resdict = json.loads(res.decode('utf-8'))
    return res.decode('utf-8')


import time
import os


def run(config, logger, cnt):
    logger.info('this is func run of mod_cam')
    # get config
    try:
        addr = config['addr']
        imgfilepath = config['imgfilepath']
        videodevice = config['videodevice']
        resolution = config['resolution']
    except:
        logger.exception('missing config para')
        exit(1)
    # capture and save a frame
    try:
        caponeframe(imgfilepath, videodevice, resolution)
    except:
        logger.exception('#{} failed to capture'.format(cnt))
        exit(1)
    logger.info('#{} captured'.format(cnt))
    #   upload a frame
    #   no need to fork
    try:
        result = uploadoneframe(addr, imgfilepath)
    except:
        logger.exception('#{} failed to upload'.format(cnt))
        exit(1)
    logger.info('#{} uploaded, result: {}'.format(cnt, result))
    exit(0)
    return 0

import os
import os.path


def fix(config, logger, exitcode):
    logger.info('this is func fix of mod_cam')
    # get config
    try:
        addr = config['addr']
        imgfilepath = config['imgfilepath']
        videodevice = config['videodevice']
        resolution = config['resolution']
    except:
        logger.exception('missing config para')
        exit(1)
    if not os.path.exits(videodevice):
        logger.error('not such device, failed to fix')
        exit(1)
    exit(0)
    return 0

import logging
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    cnt = 9527
    config = {"addr": "http://211.83.111.245/biaoben/img_receive.php",
              "imgfilepath": "/tmp/img_cam0.jpg",
              "videodevice": "/dev/video0",
              "resolution": [1280, 720]}
    run(config, logger, cnt)
    print('finished!')
