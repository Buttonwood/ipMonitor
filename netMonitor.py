#!/usr/bin/env python
# encoding: utf-8
#
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib
import json
import re
import socket
import random
import subprocess
import config
from sendmail import Mailsender

def start():
    cmd  = "/usr/sbin/iftop -nNpPts %d >/root/.src/tmp.log" % random.randint(60,240)
    print cmd
    subprocess.call(cmd,shell=True)

def end():
    cmd  = "rm -rf /root/.src/tmp.log"
    subprocess.call(cmd,shell=True)

def ip_location(ip):
    url = "http://ip.taobao.com/service/getIpInfo.php?ip="
    data = urllib.urlopen(url + ip).read()
    datadict=json.loads(data)
    for oneinfo in datadict:
        if "code" == oneinfo:
            if datadict[oneinfo] == 0:
                return (datadict["data"]["country"] + datadict["data"]["region"] + datadict["data"]["city"] + datadict["data"]["isp"]).encode("utf8")

def get_location(ip_address):
    #定义IP与域名正则
    if ":" in ip_address:
        ip_address = ip_address.split(":")[0]
    re_ipaddress = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    re_domain = re.compile(r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?')
    if re_ipaddress.match(ip_address):  #如果参数是单个IP地址
        """
        city_address = ip_location(ip_address)
        print ip_address + ":" + city_address"""
        return ip_location(ip_address)
    elif(re_domain.match(ip_address)):  #如果参数是域名
        result = socket.getaddrinfo(ip_address, None)
        ip_address = result[0][4][0]
        """
        city_address = ip_location(ip_address)
        print ip_address.strip() + ":" + city_address"""
        return ip_location(ip_address)

def ip_check(aip):
    """不是这些内网和特定ip则True"""
    return not any((aip.startswith(x) for x in ("192.168.","10.","172.","239.2.11.71","127.0.")))

def net_check(rate,threshold):
    """大于阈值则True"""
    match   = re.split(r'(\D+)',rate)
    number  = float(''.join(match[:-2]))
    unit    = match[-2]
    if unit == 'b':
        number = number*1.00/1024/1024
    elif unit == 'Kb':
        number = number*1.00/1024
    elif unit == 'Gb':
        number = number*1.00*1024
    else:
        pass
    return number>threshold

"""
iftop -nNpPts 10
"""
def msg(net):
    start()
    fh = open("/root/.src/tmp.log")
    line = fh.readline()
    msg = ""
    while line:
        if  "=>" in line:
            net_out  = line.split()#sent
            line    = fh.readline()#receive
            net_in = line.split()
            if any((ip_check(net_out[1]),ip_check(net_in[0]),net_check(net_out[-2],net["SE"]),net_check(net_in[-2],net["RE"]))):
                msg += net_out[1] + " ("+  get_location(net_out[1]) + ") sent to " + net_in[0] +  " ("+  get_location(net_in[0]) + ") rate is " + net_out[-2] + "/s and receive rate is " + net_in[-2] + "/s.\n"
        if "Total send rate" in line:
            TSE = line.split()[-2]
            if net_check(TSE,net['TSE']):
                msg += "Total send rate is " + TSE + "/s>" + net['TSE'] + "Mb/s.\n"
        if "Total receive rate" in line:
            TRE = line.split()[-1]
            if net_check(TRE,net['TRE']):
                msg += "Total receive rate is " + TRE + "/s>" + net['TRE'] + "Mb/s.\n"
        if "Total send and receive rate" in line:
            TSR =  line.split()[-1]
            if net_check(TRE,net['TRE']):
                msg += "Total send and receive rate is " + TSR + "/s>" + net['TSR'] + "Mb/s.\n"
        if "Peak rate" in line:
            PSE,PRE,PTT =  line.split()[-3::]
            if any((net_check(PSE,net['PSE']),net_check(PRE,net['PRE']),net_check(PTT,net['PTT']))):
                msg += "Peak rate （sent|received|total）is " + PSE + "|" + PRE + "|"+ PTT + "/s.\n"
        line = fh.readline()
    fh.close()
    #end()
    print msg
    if msg == '':
        sys.exit()
    else:
        mail(msg)

def mail(msg):
    mail = Mailsender()
    mail.setSmtpServer(config.mail['SMTP'])
    mail.setSender(config.mail['SENDER'],config.mail['USER'],config.mail['PASSWD'])
    mail.setReceiver(config.mail['MAILS'])
    mail.setSubject(config.mail["SUBJECT"])
    mail.setText("Testing!")
    mail.setHtml(msg)
    mail.sendMail()

def main():
    msg(config.net)

if __name__ == '__main__':
    main()
