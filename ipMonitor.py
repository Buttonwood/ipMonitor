#!/usr/bin/env python
# encoding: utf-8
import random
import subprocess
import config
import helper
import iptools
#import time
from logger import Logger
from sendmail import Mail

class ipMonitor(object):
    def __init__(self):
        super(ipMonitor, self).__init__()
        self.hostname = "{0}({1})".format(helper.get_hostname(),helper.get_local_ip())
        self.logger   = Logger('ipMonitor', 'ipMonitor.log')

    def start(self):
        agap = random.randint(10,250)
        acmd  = "/usr/sbin/iftop -nNpPts %d >iftop.log" % agap
        self.logger.info(acmd)
        subprocess.call(acmd,shell=True)
        #return agap

    def job(self,net):
        #agap = int(self.start()) + 65
        #time.sleep(agap)
        self.start()
        fh = open("iftop.log")
        line = fh.readline()
        msg = ""
        while line:
            if  "=>" in line:
                net_out = line.split()#sent
                sip_location, srate = iptools.get_location(net_out[1]),net_out[-2]
                line    = fh.readline()#receive
                net_in  = line.split()
                rip_location, rrate = iptools.get_location(net_in[0]),net_in[-2]
                if iptools.ip_iptype(net_out[1]) == 'PUBLIC' or iptools.ip_iptype(net_in[0]) == 'PUBLIC':
                    atmp = "{0}({1}) sent to {2}({3}) at avg rate {4}/s and receive at avg rate {5}/s in last 40s;".format(net_out[1],sip_location,net_in[0],rip_location,srate,rrate)
                    self.logger.info(atmp)
                    msg += atmp
                else:
                    if iptools.net_check(srate,net["SE"]):
                        atmp = "{0}({1}) sent to {2}({3}) at avg rate {4}/s > {5}Mb/s in last 40s;".format(net_out[1],sip_location,net_in[0],rip_location,srate,net["SE"])
                        self.logger.info(atmp)
                        msg += atmp
                    if iptools.net_check(rrate,net["RE"]):
                        atmp = "{0}({1}) received from {2}({3}) at avg rate {4}/s > {5}Mb/s in last 40s;".format(net_out[1],sip_location,net_in[0],rip_location,rrate,net["RE"])
                        self.logger.info(atmp)
                        msg += atmp
            if "Total send rate" in line:
                TSE = line.split()[-2]
                if iptools.net_check(TSE,net['TSE']):
                    atmp = "{0}\'s total send rate is {1}/s > {2} Mb/s in last 40s;".format(self.hostname,TSE,net['TSE'])
                    self.logger.info(atmp)
                    msg += atmp
            if "Total receive rate" in line:
                TRE = line.split()[-1]
                if iptools.net_check(TRE,net['TRE']):
                    atmp = "{0}\'s total receive rate is {1}/s > {2} Mb/s in last 40s;".format(self.hostname,TRE,net['TRE'])
                    self.logger.info(atmp)
                    msg += atmp
            if "Total send and receive rate" in line:
                TSR =  line.split()[-1]
                if iptools.net_check(TRE,net['TRE']):
                    atmp = "{0}\'s total send and receive rate is {1}/s > {2} Mb/s in last 40s;".format(self.hostname,TSR,net['TSR'])
                    self.logger.info(atmp)
                    msg += atmp
            if "Peak rate" in line:
                PSE,PRE,PTT =  line.split()[-3::]
                if any((iptools.net_check(PSE,net['PSE']),iptools.net_check(PRE,net['PRE']),iptools.net_check(PTT,net['PTT']))):
                    atmp = "{0}\'s peak rate (sent|received|total) is is {1}|{2}|{3}/s and cutoff is {4}Mb/s|{5}Mb/s|{6}Mb/s in last 40s;".format(self.hostname,PSE,PRE,PTT,net['PSE'],net['PRE'],net['PTT'])
                    self.logger.info(atmp)
                    msg += atmp
            line = fh.readline()
        fh.close()
        return msg

def makeHtml(msg):
    html = ""
    for line in msg.split(";")[0:-1]:
        html += """
        <p>
            {0}
        ;</p>""".format(helper.u_to_s(line))
    return html

def main():
    mlogger = Logger('iplogger', 'ipMonitor.log')
    tmail   = Mail(config.mail)
    ipm     = ipMonitor()
    mlogger.info("The ipMonitor starts to work ... ")
    msg     = ipm.job(config.net)
    mlogger.info("The ipMonitor ends ... ")
    if msg != '':
        mlogger.info("The MailSender starts to work ... ")
        tmail.setText("Here is the details from your host {0}".format(ipm.hostname))
        tmail.setHtml(makeHtml(msg))
        tmail.sendMail()
        mlogger.info("The MailSender ends ... ")

if __name__ == '__main__':
    main()
