#!/usr/bin/python2.6
from enterprise import SforceEnterpriseClient
from ConfigParser import SafeConfigParser
from subprocess import call
import os
import pynotify
	
def getCredentials():
    parser = SafeConfigParser()
    scriptDir = os.path.split(os.path.abspath(__file__))[0]
    credentialsFile = os.path.join(scriptDir, '..', '..', '.sfdc_credentials')
    parser.read(credentialsFile)
    username = parser.get(getGitHubBranch(), 'USERNAME')
    password = parser.get(getGitHubBranch(), 'PASSWORD')
    securitytoken = parser.get(getGitHubBranch(), 'SECURITY_TOKEN')
    return username, password, securitytoken

def apexAPILogin():
    username, password, securitytoken = getCredentials()
    scriptDir = os.path.split(os.path.abspath(__file__))[0]
    wsdlFile = os.path.join(scriptDir, '..', 'config', 'wsdl.jsp.xml')
    h = SforceEnterpriseClient(wsdlFile)
    result = h.login(username, password, securitytoken)
    header = h.generateHeader('SessionHeader')
    header.sessionId = result['sessionId']
    #ApexAPI WSDL does not have a login call. Use Enterprise WSDL to get SessionID
    #All future calls need ApexAPI WSDL
    apexFile = os.path.join(scriptDir, '..', 'config', 'apex.xml')
    ApexAPIClient = SforceEnterpriseClient(apexFile)
    ApexAPIClient.setSessionHeader(header)
    ApexAPIClient._setHeaders()
    ApexAPIClient._sforce.set_options(location = getApexAPIUrl(result.serverUrl))
    return ApexAPIClient

def getApexAPIUrl(serverUrl):
	#dynamically change the SOAP endpoint to the endpoint required for ApexAPI
	#http://www.salesforce.com/us/developer/docs/apexcode/Content/apex_api.htm
	return serverUrl.replace('/c/', '/s/')

def runTests(ApexAPIClient):
    myTest = ApexAPIClient._sforce.factory.create('RunTestsRequest')
    myTest.allTests = True
#	print myTest
	
#	compileAndTest = ApexAPIClient._sforce.factory.create('CompileAndTestRequest')
#	compileAndTest.runTestsRequest = myTest

#	print compileAndTest
	
#	testResult = ApexAPIClient._sforce.factory.create('RunTestsResult')
#	print testResult

    myResults = ApexAPIClient._sforce.service.runTests(myTest)
    notificationText = ''
    try:
        print 'Number of Tests Run: ' + str(myResults.numTestsRun)
        print 'Number of Successes: ' + str(len(myResults.successes))
        print 'Number of Failures: ' +  str(myResults.numFailures)
        print 'Time: ' + str(myResults.totalTime)
        notificationText = 'Number of Tests Run: \t' + str(myResults.numTestsRun) + ' \nNumber of Successes: \t' + str(len(myResults.successes)) + ' \nNumber of Failures: \t' + str(myResults.numFailures)
        pynotify.Notification('GSO Dharma', notificationText).show()
        if 'failures' in myResults:
            print '\n\n############ FAILURES #############'
            for failwhale in myResults.failures:
                print failwhale.name + '.' + failwhale.methodName
                print '\t' + failwhale.message
                print '\t\t' + failwhale.stackTrace.replace('\n', '\n\t\t')
    except Exception as E:
        print myResults
        print E
	
def getGitHubBranch():
    path = os.path.split(os.path.abspath(__file__))[0]
    folders = path.split(os.sep)
    return folders[-2]
myClient = apexAPILogin()
runTests(myClient)
