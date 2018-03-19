import os
import sys
from urllib2 import urlopen, URLError
import json

REMOTE_IP_GETTER = 'http://ip.taobao.com/service/getIpInfo.php?ip=myip'
LOCAL_IP_GETTER = '/tmp/___ip___'
REMOTE_IP_SETTER = 'http://xx.xxxxx.com/'

try:
    response = urlopen(REMOTE_IP_GETTER)
except URLError, e:
    if hasattr(e, 'reason'):
        print 'Error reason: ', e.reason
    if hasattr(e, 'code'):
        print 'Error code: ', e.code
else:
    try:
        jsonstr = response.read().strip()
        jsonObj = json.loads(jsonstr)
        realip = jsonObj['data']['ip']
    except Exception, e:
        print e
    else:
        try:
            ip = ''
            with open(LOCAL_IP_GETTER) as f:
                ip = f.read()
            if ip == realip:
                raise IOError('IP Change')
        except IOError, e:
            print "IOError:", str(e) , "Try to write real ip:", realip
            try:
                with open(LOCAL_IP_GETTER, 'w') as f:
                    f.write(realip)
            except IOError, e:
                print "IOError:", str(e)
            else:
                try:
                    urlopen(REMOTE_IP_SETTER + realip)
                except URLError, e:
                    print 'Error:', e.reason
                    print 'real ip:', realip

