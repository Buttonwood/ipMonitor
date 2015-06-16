#!/usr/bin/env python
# encoding: utf-8
import urllib
import json
import re
import socket
from IPy  import IP

def ip_location(ip):
    url = "http://ip.taobao.com/service/getIpInfo.php?ip="
    data = urllib.urlopen(url + ip).read()
    datadict=json.loads(data)
    for oneinfo in datadict:
        if "code" == oneinfo:
            if datadict[oneinfo] == 0:
                return (datadict["data"]["country"] + datadict["data"]["region"] + datadict["data"]["city"] + datadict["data"]["isp"]).encode("utf8")

def get_location(ip_address):
    #定义IP与域名正则,带有端口
    if ":" in ip_address:
    	ip_address = ip_address.split(":")[0]
    re_ipaddress = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    re_domain = re.compile(r'[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?')
    if re_ipaddress.match(ip_address):  #如果参数是单个IP地址
        return ip_location(ip_address)
    elif(re_domain.match(ip_address)):  #如果参数是域名
        result = socket.getaddrinfo(ip_address, None)
        ip_address = result[0][4][0]
        return ip_location(ip_address)

def ip_check(aip,ippass=[]):
    """不是这些内网和特定ip则True"""
    return not any((aip.startswith(x) for x in (["192.168.","239.2.11.71","127.0.","255.255.255.255"] + ippass)))

def ip_iptype(aip):
    if ":" in aip:
        aip = aip.split(":")[0]
    return IP(aip).iptype()

def net_check(rate,threshold):
    """大于阈值则True"""
    unet 	= {'b':1.00/1024/1024,	'Kb':1.00/1024,	'Mb':1.00,	'Gb':1.00*1024}
    match   = re.split(r'(\D+)',rate)
    number  = float(''.join(match[:-2]))
    unit    = match[-2]
    number  = number * unet.get(unit,1.00)
    return number >= threshold

def main():
	ip_list = ["192.168.2.136:46778","192.168.3.2:22","10.10.102.1","172.132.152.32:22","239.2.11.71","127.0.0.1","255.255.255.255","27.19.151.33:22",'58.49.48.96',"27.193.151.33",'58.49.49.96']
	ip_pass = ["27.19.151.33",'58.49.48.96']
	for x in ip_list:
		print("{0} => {1}".format(x,get_location(x)))
		if ip_check(x,ip_pass):
			print("{0}/{1} is passed!".format(x,ip_iptype(x)))
		else:
			print("{0}/{1} is not passed!".format(x,ip_iptype(x)))
	rates = ["100b",'2Mb','80Gb','40Kb']
	for y in rates:
		if net_check(y, 10):
			print("{0} > 10 !".format(y))
		else:
			print("{0} < 10 !".format(y))

if __name__== '__main__':
	main()
