#!/usr/bin/env python3
# -*- coding: utf-8 -*-

addr = "http://211.83.111.245/biaoben/img_receive.php"
imgfilepath = "temp/projectsperm/img.jpg"

import pygame, pygame.camera
from urllib import request, parse
import json

if __name__ == '__main__':
	#capture and save a frame
	pygame.camera.init()
	cam = pygame.camera.Camera("/dev/video0",(640,480))
	cam.start()
	img = cam.get_image()
	cam.stop()
	pygame.image.save(img,imgfilepath)
	#upload a frame
	imgfile = open(imgfilepath, 'rb')
	#reqdata = parse.urlencode([('image', imgfile.read())])
	reqdata = imgfile.read()
	imgfile.close()
	req = request.Request(addr)
	#with request.urlopen(req, data = reqdata.encode('utf-8')) as f:
	with request.urlopen(req, data = reqdata) as f:
		if f.status >= 400:
			raise ConnectionError('HTTP ERR: ', f.status)
		res = f.read()
		#resdict = json.loads(res.decode('utf-8'))
