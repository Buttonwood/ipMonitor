#!/usr/bin/env python
# encoding: utf-8

# mail
mail = {
	"MAILS"	 : ["tanhao2013@foxmail.com","tanhao2013@me.com"],
	"SMTP"   : "smtp.163.com",
	"SENDER" : "peony_wh@163.com",
	"USER"   : "peony_wh",
	"PASSWD" : "peony2014",
	"SUBJECT": "Network Flux Monitor"
}

# net
net = {
	# Each ip sent and receive threshold (Mb/s) in last 40s.
	"SE":0.1,
	"RE":0.1,
	#Total send rate
	"TSE":1,
	#Total receive rate
	"TRE":1,
	#Total send and receive rate
	"TSR":1,
	#Peak rate （sent/received/total）
	"PSE":1,
	"PRE":1,
	"PTT":1
}