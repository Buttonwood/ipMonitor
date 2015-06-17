#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    @File:      mails.py
    @Author:    Hao Tan
    @Date:      20150109
    @Email:     tanhao2013@foxmail.com
    @Desc:      A script for mails sending.
    @Refer to:  http://www.oschina.net/code/snippet_144709_13325
"""

from helper import u_to_s,get_hostname,get_local_ip
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  
from email.mime.image import MIMEImage  
import base64

class Mailsender():
    def __init__(self):
        print "Start sending the mails ..."

    def setSmtpServer(self, smtpServer):
        self.smtpserver = smtpServer

    def setSender(self, sender, username, password):
        self.sender = sender
        self.username = username
        self.password = password

    def setReceiver(self,receiver):
        self.receiver = receiver

    def setSubject(self, subject):
        self.subject = subject

    def setText(self,text):
        self.text = u_to_s(text)

    def setHtml(self,html):
        self.html = u_to_s(html)

    def sendMail(self):
        smtp = smtplib.SMTP()
        smtp.connect(self.smtpserver)
        smtp.login(self.username, self.password)  
        msg  = MIMEMultipart('alternative')
        msg['From'] = self.sender
        msg['To']   = ",".join(self.receiver)
        msg['Subject'] = self.subject
        part1 = MIMEText(self.text, 'plain')  
        part2 = MIMEText(self.html, 'html')  
        msg.attach(part1)  
        msg.attach(part2)
        smtp.sendmail(self.sender, self.receiver, msg.as_string())
        smtp.quit()

    def __del__(self):
        print "Finish sending mails !"


class Mail(object):
    def __init__(self, arg):
        super(Mail, self).__init__()
        self.mail = self.setMail(arg)
    
    def setMail(self,mail):
        amail = Mailsender()
        amail.setSmtpServer(mail.get('SMTP','smtp.163.com'))
        amail.setSender(mail.get('SENDER','peony_wh@163.com'),mail.get('USER','*******'),mail.get('PASSWD','*****'))
        amail.setReceiver(mail.get('MAILS',["tanhao2013@foxmail.com","tanhao2013@msn.cn"]))
        host_info = " From Your Host {0}|{1} ".format(get_hostname(),get_local_ip())
        amail.setSubject(mail.get('SUBJECT','A Testing Mail By ADMIN!') + host_info)
        amail.setText(host_info)
        return amail

    def setText(self,text): 
        self.mail.setText(text)

    def setHtml(self,html): 
        self.mail.setHtml(html)

    def sendMail(self):   
        self.mail.sendMail()   

def test():
    receiverList = ["tanhao2013@foxmail.com","tanhao2013@msn.cn"]
    mail = Mailsender()
    mail.setSmtpServer("smtp.163.com")
    mail.setSender("peony_wh@163.com","*******","******")
    mail.setReceiver(receiverList)
    mail.setSubject("This is a test mail!")
    mail.setText("Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org")
    mail.setHtml(""" 
<html> 
  <head></head> 
  <body> 
    <p>Hi!<br> 
       How are you?<br> 
       Here is the <a href="http://www.python.org">link</a> you wanted. 
    </p>
    <table border="1">
      <tr>
        <th>月份</th>
        <td></td>
        <th>Savings</th>
      </tr>
      <tr>
        <td>January</td>
        <td>mmm</td>
        <td>$100</td>
      </tr>
    </table> 
  </body> 
</html>  
""" )
    mail.sendMail()

def main():
    test()
    import config
    tmail = Mail(config.mail)
    tmail.setText("Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org")
    tmail.setHtml(""" 
<html> 
  <head></head> 
  <body> 
    <p>Hi!<br> 
       How are you?<br> 
       Here is the <a href="http://www.python.org">link</a> you wanted. 
    </p>
    <table border="1">
      <tr>
        <th>月份</th>
        <td></td>
        <th>Savings</th>
      </tr>
      <tr>
        <td>January</td>
        <td>mmm</td>
        <td>$100</td>
      </tr>
    </table> 
  </body> 
</html>  
""" )
    tmail.sendMail()

if __name__ == '__main__':
    main()
