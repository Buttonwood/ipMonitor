#nstall -y python-setuptools
#easy_install pip
#pip install IPy
#yum install vixie-cron crontabs -y
crontab -l
crontab -e

*/5 * * * * /root/ipMonitor/ipMonitor.py

#service crond start
#service crond stop
service crond restart
service crond reload
service crond status
