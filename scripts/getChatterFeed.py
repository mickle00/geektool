#!/usr/bin/python
from enterprise import SforceEnterpriseClient
import urllib2
#import urllib
import os
import json
import time
import keyring

def getCredentials():
    username = 'mistewart@expedia.com'
    password = keyring.get_password('GSO_Production', username)
    return username, password, ''

def getSessionId():
    username, password, securitytoken = getCredentials()
    scriptDir = os.path.split(os.path.abspath(__file__))[0]
    wsdlFile = os.path.join(scriptDir, '..', 'config', 'wsdl.jsp.xml')
    h = SforceEnterpriseClient(wsdlFile)
    result = h.login(username, password, securitytoken)
    header = h.generateHeader('SessionHeader')
    header.sessionId = result['sessionId']
#    print result
    return header.sessionId

def getChatterFeed():
    mySessionId = getSessionId()
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request('https://na8.salesforce.com/services/data/v25.0/chatter/feeds/news/me/feed-items?sort=LastModifiedDateDesc')
    #request = urllib2.Request('https://na8.salesforce.com/services/data/v25.0/chatter/feeds/company/feed-items') 
    request.add_header('Authorization: ', 'OAuth ' + mySessionId)
    response = opener.open(request).read()
    myjson = json.loads(response)
    print json.dumps(myjson, sort_keys = False, indent = 2)
   # for feedItem in reversed(myjson['items']):
   #     print feedItem['actor']['name'] +' ' + feedItem['body']['text'] 

getChatterFeed()
