#!/usr/bin/python2.7
from enterprise import SforceEnterpriseClient
from ConfigParser import SafeConfigParser
import sys
from subprocess import call
import urllib2
import json
import keyring
import os
import texttable

## TODO: Add queryMore to recieve more than 2k records.
## http://www.salesforce.com/us/developer/docs/api_rest/index_Left.htm#StartTopic=Content/resources_query.htm
## TODO: look at CSV creation, and or enclosing in doublequotes

def getCredentials():
	#parser = SafeConfigParser()
	#parser.read('/home/mikey/Expedia/source_control/GSO_Production/sfdc_credentials')
	#username = parser.get('sfdc_production', 'USERNAME')
	#password = parser.get('sfdc_production', 'PASSWORD')
	#securitytoken = parser.get('sfdc_production', 'SECURITY_TOKEN')
	#return username, password, securitytoken
	username = 'mistewart@expedia.com'
	password = keyring.get_password('GSO_Production', username)
	return username, password, ''

def doLogin():
	username, password, securitytoken = getCredentials()
	h = SforceEnterpriseClient('../config/wsdl.jsp.xml')
	result = h.login(username, password, securitytoken)
	return result['sessionId']

def doQuery():
	queryString = sys.argv[1]
	queryString = queryString.replace(' ', '+')
	sessionId = doLogin()
	curlScript = "https://na8.salesforce.com/services/data/v24.0/query/?q="+queryString+ " -H 'Authorization: OAuth " + sessionId + "' -H 'X-PrettyPrint:1'"
	#print curlScript
	print(call('/usr/bin/curl ' + curlScript, shell=True))

def doUrllib():
	queryString = sys.argv[1]
	queryString = queryString.replace(' ', '+')
	sessionId = doLogin()
	myURL = "https://na8.salesforce.com/services/data/v24.0/query/?q="+queryString 
	req = urllib2.Request(myURL)
	req.add_header('Authorization', 'OAuth '+sessionId)
	req.add_header('X-PrettyPrint', 1)
	res = urllib2.urlopen(req)
	responseString = res.read()
	#JSONtoCSV(responseString)
	#print responseString
	printTextTable(responseString)	

def JSONtoCSV(myJSON):
	jsonDump = json.loads(myJSON)
	rawJSON = open('rawJSON.txt', 'w')
	rawJSON.write(myJSON)
	rawJSON.close()
	if len(sys.argv) == 3:
		fileName = sys.argv[2]
	else:
		fileName = ''
#	print 'fileName', fileName
	outputString = ''
	keys = []
	for key in jsonDump['records'][0]:
		if key != 'attributes':
			keys.append(key)
			outputString += key +  ','
	outputString = outputString[:-1]
	outputString += '\n'

	for record in jsonDump['records']:
		for key in keys:
			if record[key] != None:
				outputString += str(record[key])
			outputString += ','

		outputString = outputString[:-1]
		outputString += '\n'

	if fileName != '':
		newFile = open(fileName, 'wb')
		newFile.write(outputString.encode('utf8', 'replace'))
		newFile.close()
	#else:
	#	print outputString

def printTextTable(myJSON):
	table = texttable.Texttable()
	#fakeJSON = open('case.JSON', 'r')
	jsonDump = json.loads(myJSON)
	keys = []
	#TODO: Get more than one level of nested JSON arrays from related objects
	for key in jsonDump['records'][0]:
		if key != 'attributes': 
			if type(jsonDump['records'][0][key]) != type({}):
				keys.append(key)
			else: 
				for subkey in jsonDump['records'][0][key]:
					if subkey != 'attributes':
						keys.append(key + '.' + subkey)
	tableHeaders = []
	for key in keys:
		tableHeaders.append(str(key))
	table.add_row(tableHeaders)
	
	for record in jsonDump['records']:
		outputList = []
		for key in keys:
			if '.' in key:
				key, subkey = key.split('.')
				outputList.append(record[key][subkey])

			elif record[key] != None: 
				outputList.append(str(record[key]))
		table.add_row(outputList)
	print table.draw() + "\n" 
doUrllib()
