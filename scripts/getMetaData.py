#!/usr/bin/python2.6
from enterprise import SforceEnterpriseClient
from ConfigParser import SafeConfigParser
import base64
import zipfile
import os
from time import strftime
from time import sleep
from subprocess import call

# GITHUB Branch must equal Directory Name
# Ex. /home/mikey/Expedia/source_control/GSO_Dharma points to GSO_Dharma github branch

	
def getCredentials():
	parser = SafeConfigParser()
	parser.read('../.sfdc_credentials')
	username = parser.get(getGitHubBranch(), 'USERNAME')
	password = parser.get(getGitHubBranch(), 'PASSWORD')
	securitytoken = parser.get(getGitHubBranch(), 'SECURITY_TOKEN')
	return username, password, securitytoken

def metaDataLogin():
	username, password, securitytoken = getCredentials()
	h = SforceEnterpriseClient('config/wsdl.jsp.xml')
	result = h.login(username, password, securitytoken)
	header = h.generateHeader('SessionHeader')
	header.sessionId = result['sessionId']
	#MetaData WSDL does not have a login call. Use Enterprise WSDL to get SessionID
	#All future calls need metadata WSDL
	metaDataClient = SforceEnterpriseClient('config/metadata.xml')
	metaDataClient.setSessionHeader(header)
	metaDataClient._setHeaders()
	metaDataClient._sforce.set_options(location = result.metadataServerUrl)
	return metaDataClient

def buildMetaDataPackage(metaDataClient):
	#obj = h._sforce.factory.create('ListMetadataQuery')
	package = metaDataClient._sforce.factory.create('Package')
	package.types = [buildPackageTypeMembers(metaDataClient, ['CustomObject', 'ApexClass', 'ApexTrigger', 'ApexPage', 'ApexComponent','StaticResource', 'StandardObject','Profile', 'Layout','Workflow','PermissionSet','Role','ReportType','Queue','Folder','CustomTab','Group','CustomSite'])]
	return package

def buildPackageTypeMembers(metaDataClient, listOfMembers):
	packageMemberList = []
	for member in listOfMembers:
		if (member == 'StandardObject'):
			newMember = buildStandardObjectMembers(metaDataClient)
		else:
			newMember = metaDataClient._sforce.factory.create('PackageTypeMembers')
			newMember.name = member
			newMember.members = '*'
		packageMemberList.append(newMember)
	return packageMemberList

def buildStandardObjectMembers(metaDataClient):
	newMember = metaDataClient._sforce.factory.create('PackageTypeMembers')
	newMember.name = 'CustomObject'
	newMember.members = ['Account', 'Case', 'Contact']
	return newMember
		
def buildMetaDataRequest(metaDataClient):
	RetrieveRequest = metaDataClient._sforce.factory.create('RetrieveRequest')
	RetrieveRequest.unpackaged = [buildMetaDataPackage(metaDataClient)]
	RetrieveRequest.singlePackage = True
	RetrieveRequest.apiVersion = 24.0
	result = metaDataClient._sforce.service.retrieve([RetrieveRequest])
	jobId = result['id']
	return jobId

def checkJobStatus(metaDataClient, jobId):
	jobStatus = metaDataClient._sforce.service.checkStatus([jobId])

	while jobStatus[0].done == False:
		sleep(5)
		print jobStatus[0].state
		jobStatus = metaDataClient._sforce.service.checkStatus([jobId])
	
def getMetaData(pushToGit):
	metaDataClient = metaDataLogin()
	jobId = buildMetaDataRequest(metaDataClient)
	checkJobStatus(metaDataClient, jobId)
	handleResult(metaDataClient, jobId)
	if pushToGit: 
		pushToGitHub()

def handleResult(metaDataClient, jobId):
	jobResult = metaDataClient._sforce.service.checkRetrieveStatus(jobId)
	handleZipFile(jobResult.zipFile)
	print 'Complete'

def handleZipFile(attachment):
	newestFile = decodeZipFile(attachment)
	z = zipfile.ZipFile(newestFile)
	z.extractall('src/')

def decodeZipFile(attachment):
	filetime = strftime("%Y-%m-%d-%I%M-%p-%Z")
	filename = 'backup/Export_' + filetime + '.zip'
	newFile = open(filename, 'wb')
	newFile.write(base64.b64decode(attachment))
	newFile.close()
	return filename

def pushToGitHub():
	call(['/bin/sh', 'scripts/pushToGithub.sh'])

def getGitHubBranch():
	#return os.path.split(os.path.dirname(os.path.realpath(__file__)))[1]
	#getParentDirectory
#	return os.path.split(os.path.abspath(os.path.pardir))[1]
	localFolder = os.path.split(os.getcwd())[1]
	if localFolder == 'scripts':
		localFolder = os.path.split(os.path.abspath(os.path.pardir))[1]
	return localFolder

getMetaData(False)
