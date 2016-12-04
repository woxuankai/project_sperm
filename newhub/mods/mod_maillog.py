#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import os.path
import time
# delete file if last modification is earlier than time_delete
def is_old_file(filepath, lag):
    # if lag is negative, the the file is never old
    if (lag >= 0) and (lag < time.time() - os.path.getmtime(filepath)):
        return True
    else:
        return False

def pick_old_files(files,lag):
    oldfiles = set()
    for onefile in files:
        if is_old_file(onefile, lag):
            oldfiles.add(onefile)
    return oldfiles

def delete_file(filepath):
    os.remove(filepath)


import smtplib
import logging


def smtp_sendmail(config, msg):
    # smtp configs
    account = config['account']
    passwd = config['passwd']
    server = config['server']
    server_port = config['server_port']
    assert(type(server_port) == int)
    encryption = config['encryption']
    assert(type(encryption) == bool)
    from_addr = config['from_addr']
    to_addrs = config['to_addrs']
    assert(type(to_addrs) == list)
    # msg may be a string containing characters in the ASCII range, \
    # or a byte string. \
    # A string is encoded to bytes using the ascii codec, \
    # and lone \r and \n characters are converted to \r\n characters.
    # A byte string is not modified.
    smtp = smtplib.SMTP(server, server_port)
    smtp.ehlo()
    if encryption:
        smtp.starttls()
        smtp.ehlo()
    smtp.login(account, passwd)
    smtp.sendmail(from_addr, to_addrs, msg.as_string())
    smtp.quit()

import email.mime.text


def email_log2mail(config, textfile):
    COMMASPACE = ', '
    from_addr = config['from_addr']
    to_addrs = config['to_addrs']
    assert(type(to_addrs) == list)
    with open(textfile, 'r') as fp:
        msg = email.mime.text.MIMEText(fp.read())
    msg['Subject'] = textfile
    msg['To'] = COMMASPACE.join(to_addrs)
    msg['From'] = from_addr
    return msg

import os
import os.path


def run(config, logger, cnt):
    logger.info('this is func run of mod_maillog')
    # get config
    try:
        time_delete = config['time_delete']
        assert(type(time_delete) == int)
        ifsend = config['ifsend']
        assert(type(ifsend) == bool)
        logspath = config['logspath']
        assert(type(logspath) == list)
        for onedir in logspath:
            assert(os.path.isdir(onedir))
        emailconfig = config['email']
        assert(type(emailconfig) == dict)
    except:
        logger.exception('missing config para or of wrong format')
        exit(1)
    # fetch files
    try:
        logfiles = set()
        for onedir in logspath:
            for onefile in os.listdir(onedir):
                onefile = os.path.join(onedir, onefile)
                if os.path.isfile(onefile) and not os.path.islink(onefile):
                    logfiles.add(onefile)
        oldfiles = pick_old_files(logfiles, time_delete)
    except:
        logger.exception('failed to fetch all log files')
        exit(1)
    logger.info('gathered log files, total {}, old {}'.format(len(logfiles), len(oldfiles)))
    for onelog in oldfiles:
        logger.info('processing file {}'.format(onelog))
        # send log files by email
        try:
            # form a email
            msg = email_log2mail(emailconfig, onelog)
            # send it 
            smtp_sendmail(emailconfig, msg)
        except:
            logger.exception('failed to  email')
            continue
        logger.info('sent')
        # delete old log files
        try:
            delete_file(onelog)
        except:
            logger.exception('failed to delete')
            continue
        logger.info('deleted')
    logger.info('gone throught all old log files')
    
    logger.info('daemon exit now')
    exit(0)
    return 0

import os, os.path
def fix(config, logger, exitcode):
    logger.info('this is func fix of mod_mail')
    exit(0)
    return 0

import logging
if __name__ == '__main__':
    logger=logging.getLogger(__name__)
    ch=logging.StreamHandler()
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    cnt=9528
    config={\
                "email":\
                {\
                    "account": "one_mail_addr@163.com",\
                    "passwd": "1authcode",\
                    "server": "smtp.163.com",\
                    "server_port": 25,\
                    "encryption": False,\
                    "from_addr": "one_mail_addr@163.com",\
                    "to_addrs": ["woxuankai@gmail.com"]\
                },\
                "time_delete":80,\
                "ifsend":True,\
                "logspath": ["/var/log/project_sperm/"]\
            }
    run(config, logger, cnt)
    print('finished!')
