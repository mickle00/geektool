#!/usr/bin/python
from enterprise import SforceEnterpriseClient
import urllib2
import urllib
import os
import json
import time
import keyring

f = open('/Users/Mikey/geektool/tmp/chatter.JSON', 'r')
myjson = json.loads(f.read())

#print json.dumps(myjson, sort_keys = False, indent = 2)
myItem = myjson['items'][0]
print myItem['body']['text']
for comment in myItem['comments']['comments']:
	print '\t' + str(comment['body']['text'])
