#!/usr/bin/env python3
# -*- coding: utf-8 -*-

addr = "http://211.83.111.245/biaoben/img_receive.php"
imgfilepath = "/tmp/img.jpg"

import pygame, pygame.camera
from urllib import request, parse
import json

def caponeframe(imgpath, dev, resolution):
	try:	
		pygame.camera.init()
		cam = pygame.camera.Camera(dev,resolution)
		cam.start()
		img = cam.get_image()
		cam.stop()
	except Exception as e:
		print('capture failed')
		print('details: ',e)
		raise
	try:
		pygame.image.save(img,imgpath)
	except Exception as e:
		print('save image failed')
		print('details: ',e)
		raise
	return 0

def uploadoneframe(serveraddr,imgpath):
	imgfile = open(imgpath, 'rb')
	#reqdata = parse.urlencode([('image', imgfile.read())])
	reqdata = imgfile.read()
	imgfile.close()
	req = request.Request(serveraddr)
	#with request.urlopen(req, data = reqdata.encode('utf-8')) as f:
	with request.urlopen(req, data = reqdata) as f:
		if f.status >= 400:
			raise ConnectionError('HTTP ERR: ', f.status)
		res = f.read()
		#resdict = json.loads(res.decode('utf-8'))
	return res.decode('utf-8')


if __name__ == '__main__':
	#capture and save a frame
	caponeframe(imgpath=imgfilepath, dev="/dev/video1", resolution=(640,480))
	#upload a frame
	#result = uploadoneframe(addr, "../testimgs/1.jpg")
	#result = uploadoneframe(addr, "./postdata.py")
	#print(result)
	#uploadoneframe(addr, imgfilepath)

