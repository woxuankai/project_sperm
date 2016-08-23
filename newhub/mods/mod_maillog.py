#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import os.path
import time
# delete file if last modification is earlier than time_delete


def delete_old_file(filepath, time_delete):
    if time_delete < 0:
        return False
    lag = time.time() - os.path.getmtime(filepath)
    if lag > time_delete:
        os.remove(filepath)
        return True
    return False


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
    time_delete = config['time_delete']
    assert(type(time_delete) == int)
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
                if os.path.isfile(onefile):
                    logfiles.add(onefile)
    except:
        logger.exception('failed to fetch all log files')
        exit(1)
    logger.info('gathered log files, total {}'.format(len(logfiles)))
    # send log files by email
    try:
        for onelog in logfiles:
            logger.info('forming and sending log file: {}'.format(onelog))
            # form a email
            msg = email_log2mail(emailconfig, onelog)
            smtp_sendmail(emailconfig, msg)
            logger.info('done')
    except:
        logger.exception('failed to form or send emai'))
        exit(1)
    logger.info('successfully sent all log files')
    # delete old(not the newest) log files
    for onefile in logfiles:
        try:
            ifdelete=time_delete(onefile, time_delete)
        except:
            logger.exception('failed to delete log file: {}'.format(onefile))
        else:
            logger.info('delete the logfile {} ? {}'.format(onefile, ifdelete))
    # exit
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
                "logspath": ["/var/log/project_sperm/"]\
            }
    run(config, logger, cnt)
    print('finished!')
