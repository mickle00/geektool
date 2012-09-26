#!/usr/bin/python2.7
from enterprise import SforceEnterpriseClient
from ConfigParser import SafeConfigParser
import sys
from subprocess import call
import urllib2
import urllib
import json
import keyring
import os
	
def getCredentials():
    username = 'mistewart@expedia.com'
    password = keyring.get_password('GSO_Production', username)
    return username, password, ''

def doLogin():
	username, password, securitytoken = getCredentials()
        scriptDir = os.path.split(os.path.abspath(__file__))[0]
        wsdlFile = os.path.join(scriptDir, '..', 'config', 'wsdl.jsp.xml')
        h = SforceEnterpriseClient(wsdlFile)
	result = h.login(username, password, securitytoken)
	return result['sessionId']

def doUrllib(queryString):
	queryString = queryString.replace(' ', '%20')
	sessionId = doLogin()
	myURL = "https://na8.salesforce.com/services/data/v24.0/query/?q="+queryString 
	req = urllib2.Request(myURL)
	req.add_header('Authorization', 'OAuth '+sessionId)
	req.add_header('X-PrettyPrint', 1)
	res = urllib2.urlopen(req)
	return res.read()

def parseCaseJSON(jsonResponse):
    output = open('../tmp/cases.txt','w')
    output.write('\n My Open Cases\n')
    output.write('----------------\n')
    jsonResponse = json.loads(jsonResponse)
    if (jsonResponse['totalSize'] > 0):
        for record in jsonResponse['records']:
            output.write(record['Status'] + '\t' + record['CaseNumber'] + '\t' + record['Subject'])
	    output.write('\n')
    output.close()


def parseProjectJSON(jsonResponse):
    output = open('../tmp/log.txt','w')
    output.write('\n My Open Projects\n')
    output.write('----------------\n')
    jsonResponse = json.loads(jsonResponse)
    if (jsonResponse['totalSize'] > 0):
        for record in jsonResponse['records']:
            output.write('{0: <20}{1}'.format(record['Status__c'], record['Project_Name__c']))
	    output.write('\n')
    output.close()
	    
def parseCaseImage(jsonResponse):
    jsonResponse = json.loads(jsonResponse)
    if (jsonResponse['totalSize'] > 0):
	chartVals = unicode('')
	chartNames = unicode('')
        for record in jsonResponse['records']:
	    #print record['Name'] + '\t' + str(record['total'])
	    chartVals += str(record['total']) + ','
            chartNames += str(record['Name']) + ' (' + str(record['total']) + ')|'

	chartVals = chartVals[:-1]
	chartNames = chartNames [:-1]
        chartUrl = "https://chart.googleapis.com/chart?cht=p3&chd=t:" + chartVals + "&chco=0000FF&chs=750x300&chl=" + chartNames + "&chf=bg,s,000000"
	chartUrl = chartUrl.replace(' ', '%20')
	#print chartUrl
	chartFile = urllib2.urlopen(chartUrl)
        output = open('../tmp/image.png','wb')
        output.write(chartFile.read())
        output.close()

def getCaseImage():
    #https://chart.googleapis.com/chart?cht=p3&chd=t:90,10&chs=750x300&chdl=Hello|World&chf=bg,s,000000 
    #chdl=lables
    #chd=t: values
    #TODO: INCLUDE Closed-Reply
    allCaseQuery = "SELECT%20count(id)%20total%2C%20owner.name%20from%20Case%20WHERE%20RecordTypeId%20%3D%20'012C00000004XXi' AND isClosed=FALSE%20GROUP%20BY%20Owner.Name"
    parseCaseImage(doUrllib(allCaseQuery))

caseQuery = "SELECT Id, CaseNumber, Status, Subject FROM Case WHERE OwnerId = '005C0000003oJCT' AND (isClosed = FALSE OR Status ='Closed - Reply')"  
parseCaseJSON(doUrllib(caseQuery))
projectQuery = "SELECT Id, Name, Project_Name__c, Status__c FROM PM_Project__c WHERE (OwnerId = '005C0000003oJCT' OR Developer__c = '005C0000003oJCT') AND Status__c NOT IN ('Completed', 'Cancelled') ORDER BY Status__c"
parseProjectJSON(doUrllib(projectQuery))

getCaseImage()
