#!/usr/bin/env python
# encoding: utf-8
from ipMonitor import ipMonitor,makeHtml
import config
import time
from logger import Logger
from sendmail import Mail
from threading import Timer
import time

timer_interval = 300
mlogger = Logger('mainlogger', 'ipMonitor.log')
ipm     = ipMonitor()
tmail   = Mail(config.mail)

def test(): 
    mlogger.info("The ipMonitor starts to work ... ")
    msg     = ipm.job(config.net)
    mlogger.info("The ipMonitor ends ... ")
    if msg != '':
        mlogger.info("The MailSender starts to work ... ")
        tmail.setText("Here is the details from your host {0}".format(ipm.hostname))
        tmail.setHtml(makeHtml(msg))
        tmail.sendMail()
        mlogger.info("The MailSender ends ... ")

def main():
	t=Timer(timer_interval,test)
	t.start()
	
if __name__ == '__main__':
	main()