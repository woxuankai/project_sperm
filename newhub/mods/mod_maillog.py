#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib, logging
def smtp_sendmail(config, msg):
	#smtp configs
	account = config['account']
	passwd = config['passwd']
	server = config['server']
	server_port = config['server_port']
	assert(type(smtp_server_port) == int)
	from_addr = config['from_addr']
	to_addrs = config['to_addrs']
	assert(type(to_addrs) == list)

	smtp = smtplib.SMTP(smtp_server, smtp_server_port)
	smtp.login(account, passwd)
	smtp.sendmail(from_addr, to_addrs, msg)
	smtp.quit()




import mail, smtplib
import os, os.path
def run(config, logger, cnt):
	logger.info('this is func run of mod_maillog')
	#get config
	try:
		logspath = config['logspath']
		assert(type(logspath) == list)
	except:
		logger.exception('missing config para or wrong format')
		exit(1)
	#form a mail
	try:
		caponeframe(imgfilepath, videodevice, resolution)
	except:
		logger.exception('#{} failed to capture'.format(cnt))
		exit(1)
	logger.info('#{} captured'.format(cnt))
	#send a mail



def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 邮件对象:
msg = MIMEMultipart()
msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

# 邮件正文是MIMEText:
msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))

# 添加附件就是加上一个MIMEBase，从本地读取一个图片:
with open('/Users/michael/Downloads/test.png', 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('image', 'png', filename='test.png')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='test.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)




	try:
		result = uploadoneframe(addr, imgfilepath)
	except:
		logger.exception('#{} failed to upload'.format(cnt))
		exit(1)
	logger.info('#{} uploaded, result: {}'.format(cnt, result))
	exit(0)
	return 0

import os, os.path
def fix(config, logger, exitcode):
	logger.info('this is func fix of mod_cam')
	#get config
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
if __name__=='__main__':
	logger = logging.getLogger(__name__)
	ch = logging.StreamHandler()
	logger.addHandler(ch)
	logger.setLevel(logging.INFO)
	cnt=9528
	config={}
	run(config, logger, cnt)
	print('finished!')
