#!/usr/bin/python2.6
import json
import time
import urllib2
from enterprise import SforceEnterpriseClient
from ConfigParser import SafeConfigParser
import sys
from xml.dom.minidom import parseString
import csv
from datetime import datetime

instanceURL = 'na8'
allQueries = []

##Case
allQueries.append("SELECT of_Cases__c, AccountId, Account_Market__c, Accounting_Assigned_To__c, Activated_By_Market_Manager_Date__c, Activated_Date__c, Activation_Type__c, Added_to_Project_Pipeline__c, Additional_Information__c, Additional_Status__c, Adjusted_Case_Age__c, Adjustment_Reason__c, Agency_Model__c, Allocated__c, Amount_Recovered__c, Approved_Amount_in_USD__c, AssetId, Availability_Entered_Date__c, Brand_Lookup__c, Brand__c, BusinessHoursId, Business_Impact__c, Cancellation_Policy_Received_Date__c, Carrier_Fare_Filed_Date__c, Case_Age_days__c, Case_Age_In_Business_Hours__c, Case_Category__c, Id, CaseNumber, Origin, Case_Re_Opened_By__c, Reason, Case_Time__c, Type, Chain__c, IsClosed, ClosedDate, IsClosedOnCreate, IsSelfServiceClosed, SuppliedCompany, ContactId, Contact_Account_Lookup_Results__c, Contacts_Entered_Date__c, Content_Type__c, CreatedById, CreatedDate, DM_Case__c, DM_Group__c, DM_Integration_Key__c, DM_Priority__c, Date_Case_Was_Re_Opened__c, Date_Effective_Email_Format__c, Date_of_Decision__c, Date_of_First_Response__c, Date_of_Request__c, Date_photos_content_went_live__c, Declined_Amount_in_USD__c, IsDeleted, Department__c, Description, Description_Rich_Text__c, Dispute_Amount__c, EEM_Activation_SLA__c, Earliest_Guest_Arrival__c, SuppliedEmail, Email_Button__c, Email_Recipients__c, Error_Begin_Date__c, Error_Fix_Date__c, IsEscalated, GSO_Contract__c, Google_Translate__c, Guest_Priority__c, Ids_Requested__c, Include_All_Bookings__c, Incorrect_Transfer_SR_T2_3_only__c, Internal_Reporting_Decision__c, Investigation__c, Involved__c, Language__c, Last_Chaser_Email_Sent_Date__c, Last_Chaser_Phone_Call_Date__c, Last_Commented_On__c, LastModifiedById, LastModifiedDate, Last_Status_Change__c, Level_of_Effort__c, Lodging_Operations_Agent__c, MM_Can_Do__c, Management_s_Decision__c, Market_Manager__c, Market_Manager_Email__c, Market_Manager_Phone__c, Met_SLA__c, Method_Detail__c, SuppliedName, HasCommentsUnreadByOwner, No_of_Bookings__c, Non_Responsive_Date__c, Number_of_Chaser_Emails__c, Number_of_Chaser_Phone_Calls__c, Number_of_Denials__c, DS_Number_of_Offerings__c, Number_of_Changes__c, OFID__c, Offer__c, Offer_Name__c, Office_Location__c, Operational_Unit__c, Original_Invoiced_Date__c, Original_Invoicing_Method__c, Other_Reference_ID__c, OwnerId, PS_Assigned_To__c, PSG_Case_Id__c, PSG_Case_Number__c, PSG_Owner_Email__c, PSG_Owner_Name__c, PSG_Record_Type__c, PSG_Status__c, ParentId, Path__c, SuppliedPhone, Points_of_Sale__c, Post_Closure_Report__c, Prevent_Contact_Lookup__c, Previously_Settled__c, Primary_Category__c, Priority, Proof_of_Submission__c, Rank__c, Rates_Entered_Date__c, Reason_Missed_SLA__c, RecordTypeId, Referring_Bug_ID__c, Referring_Bug_Tracker__c, Region__c, Relocation_Reason__c, Relocation_Type__c, Request_Type__c, Requestor__c, Resolution__c, Resolution_Type__c, Responsible_for_Error__c, Review_Status__c, SLA_Due_Date_ECD__c, Search_booking_date_end__c, Search_booking_date_start__c, Secondary_Category__c, HasSelfServiceComments, Selling_Model__c, Send_Auto_Response__c, Severity__c, Stack_Rank__c, Status, Sub_reason__c, Subject, Super_Region__c, Super_Region_Lookup__c, SuperRegion__c, SystemModstamp, Task_Category__c, Team__c, TempOwnerId__c, Time_With_Customer__c, Time_With_Support__c, To_Train_Date__c, Total_Amount_Requested_in_USD__c, Total_Call_Duration__c, Total_Guests__c, Total_Number_of_Bookings__c, Translated_Description__c, Type_of_Booking__c, Type_of_Error__c, Unresolved_Guests__c, Vendor_ID__c, IsVisibleInSelfService, Welcome_Email_Sent_Date__c FROM Case WHERE RecordTypeID != '012C00000004XXiIAM'")

##Account
allQueries.append("SELECT of_Accounts__c, ARI_Enabled__c, Description, Fax, Id, Name, AccountNumber, Phone, Rating, Site, Type, Active_Connections__c, AnnualRevenue, Assigned_Star_Rating__c, BillingCity, BillingCountry, BillingState, BillingStreet, BillingPostalCode, Booking_Delivery_Method__c, Brand__c, Chain__c, Closest_Airport__c, Contract_Manager_2005__c, Contract_Manager_2003__c, Contract_Manager_2004__c, Contract_Manager_2006__c, Contract_Manager_2007__c, Contract_Manager_2008__c, Contract_Manager_2009__c, Contract_Manager_2010__c, Contract_Manager_2011__c, Contract_Manager_Upside_2011__c, Contract_Manager_Upside_2012__c, Contract_Solicitation_2011__c, Contract_Solicitation_2012__c, Contract_Term__c, Contract_Types__c, Contracted_Name__c, CreatedById, CreatedDate, DS_Admintool_VNID__c, IsDeleted, Destination_Management__c, Destination_Management_Group__c, Destination_Management_Priority__c, Docusign_ID__c, EAN_Id__c, EQC_Addendum_CM__c, ESR_Structure_Type__c, ESR_or_GDS__c, ESR_Merchant_Venere_ID__c, ETP_Eligible__c, EXPE_Last_day_of_inventory__c, NumberOfEmployees, Expedia_Hotel_Id__c, Expedia_Virtual_Card__c, ExpediaPay_Last_Used_Date__c, ExpediaPay_Status__c, External_Account_Id__c, Fallback_Method__c, Fax_to_Email_Address__c, HIMS_Stop_Sell__c, H_S_Contact__c, Health_Safety_Gas_Status__c, Health_Safety_Status__c, Hotwire_Id__c, IAN_Id__c, Industry, LastActivityDate, LastModifiedById, LastModifiedDate, Latitude__c, Longitude__c, MM_Territory__c, Market__c, Market_Manager_Email__c, Market_Manager_Name__c, Market_Manager_Phone__c, MasterRecordId, Number_of_rooms__c, On_Expedia_Pay__c, OwnerId, Ownership, PSG_Language__c, PSG_Lead_Account__c, PSG_Market_Id__c, PSG_Record_Type__c, PSG_Region_Id__c, PSG_Status__c, PSG_Strategic_Account__c, PSG_Submarket_Id__c, ParentId, Price_Level__c, QL2_Id__c, RecordTypeId, Region__c, Request_Venere_ID_Date__c, Request_Venere_ID__c, Sic, ShippingCity, ShippingCountry, ShippingState, ShippingStreet, ShippingPostalCode, Star_Rating_Review_ID__c, Star_Rating_Structure_Type__c, Status__c, Stop_Sell_Reason__c, Stop_Sell_Start_Date__c, Submarket__c, Super_Region__c, SystemModstamp, TickerSymbol, Vendor_Code__c, Vendor_Id__c, Venere_Commission__c, Venere_Contract_Status__c, Venere_Hotel_Email__c, Venere_Id__c, Venere_Last_Activation_Date__c, Venere_Last_Date_Inventory__c, Venere_Page_Status__c, inserted__c, Venere_Status__c, Venere_Structure_Type__c, Venere_EEM_Availability_Policy__c, Venere_EEM_Hotel_Login__c, Venere_EEM_Last_Contract_Signed_Date__c, View_on_Expedia__c, Website, Wholesaler_Bed_bank_representation__c FROM Account")

##Account Contact
allQueries.append("SELECT Account__c, Name, Active__c, Contact__c, CreatedById, CreatedDate, IsDeleted, Inactive_Date__c, Integration_Status__c, LastActivityDate, LastModifiedById, LastModifiedDate, Number__c, PSG_Account_Id__c, PSG_Contact_Id__c, Primary_Content_Contact__c, Id, SystemModstamp, Unique_Key__c FROM Account_Contact__c")

##Contact
allQueries.append("SELECT AccountId, AssistantName, AssistantPhone, Birthdate, Fax, Phone, Case_Priority__c, Description, Id, Contact_Preference__c, CreatedById, CreatedDate, IsDeleted, Department, DoNotCall, Email, EmailBouncedDate, EmailBouncedReason, HasOptedOutOfEmail, HasOptedOutOfFax, FirstName, Name, Gender__c, Health_Safety_Contact__c, HomePhone, Integrated_With_PSG__c, Integration_Contact_Key__c, LastActivityDate, LastModifiedById, LastModifiedDate, LastName, LastCURequestDate, LastCUUpdateDate, LeadSource, MailingCity, MailingCountry, MailingState, MailingStreet, MailingPostalCode, MasterRecordId, MobilePhone, OtherCity, OtherCountry, Other_Email__c, Other_Fax__c, OtherPhone, OtherState, OtherStreet, OtherPostalCode, OwnerId, Preferred_Language__c, Prevent_Case_Auto_Association__c, RecordTypeId, ReportsToId, Role__c, Salutation, SystemModstamp, Title FROM Contact")

##Case Comment
allQueries.append("SELECT CommentBody, Id, CreatedById, CreatedDate, IsDeleted, LastModifiedById, LastModifiedDate, ParentId, IsPublished, SystemModstamp FROM CaseComment")

##Guest
allQueries.append("SELECT Paid_by_Expedia__c, Paid_by_Hotel__c, Age_days__c, Arrival_Date__c, Assigned_Office__c, Auto_Notification_Status__c, Booking_Net_Difference__c, CS_Supervisor_Cost_Approval__c, Case__c, Check_Out_Date__c, Closed__c, Closed_Date_Time__c, Coupon_Amount__c, CreatedById, CreatedDate, Customer_Payout_Amount__c, IsDeleted, Difference_Absorbed_By__c, Expedia_Booking_ID__c, External_Guest_Id__c, Name, Guest_Email__c, Hotel_Confirmation_Number__c, Hotel_Shared_Cost__c, Language__c, Last_4_Digits_of_CC__c, LastActivityDate, LastModifiedById, LastModifiedDate, Last_Modified_Date_Time__c, Lodging_Operations_Agent_Lookup__c, New_Booking_Rate__c, New_Booking_Total__c, New_Expedia_Booking_ID__c, New_Vendor__c, New_Room_Type__c, Number_of_Nights__c, Opaque_Booking__c, Original_Book_Date__c, Original_Booking_Rate__c, Original_Booking_Total__c, Original_Hotel_Vendor_ID__c, Original_Hotel_Confirmation__c, Original_Room_Type__c, Original_Taxes_Fees__c, Other_Relocation_Cost__c, New_Hotel_Name_if_out_of_network__c, PGI_Job_ID__c, Person_Who_Confirmed_Availability__c, Priority__c, Id, RecordTypeId, Relocation_Email_New_Property_Details__c, Relocation_Reason__c, Relocation_Type__c, Status__c, Alternate_Vendor__c, SystemModstamp, TMP_Old_Id__c, Time_to_Arrival__c, Title_Person_Confirmed_Availability__c, Trans_Parking_Fees__c, Travel_Product__c, User__c, Was_Expedia_CC_used__c, Wholesaler_Bed_Bank_Representation__c FROM Guest__c")

##Connection
allQueries.append("SELECT Account__c, Account_Location__c, Account_Market_Manager_Name__c, Account_Name__c, Account_Repco__c, Name, Connectivity_System__c, Connectivity_System_Vendor__c, CreatedById, CreatedDate, IsDeleted, Expedia_ID__c, Go_Date__c, Integration_Connection_Key__c, LastActivityDate, Last_Interaction__c, LastModifiedById, LastModifiedDate, Number_of_Enrollment_Chasers__c, Number_of_Mapping_Chasers__c, PSG_Account_ID__c, Platform__c, Id, Status__c, SystemModstamp, Type__c, Venere_Id__c FROM Connection__c")

##Connectivity System
allQueries.append("SELECT Booking_Conf__c, Connectivity_Knowledge_Base__c, Name, Connectivity_System_Type__c, Connectivity_Vendor__c, CreatedById, CreatedDate, IsDeleted, Description__c, EQC_Development_Progress__c, EQC_Go_Date__c, EQC_Preferred_Partner__c, EQC2__c, Expedia_Connect__c, Expedia_Quick_Connect__c, Expedia_Virtual_Card__c, External_Connectivity_System_ID__c, Interface__c, LAR_Supported__c, LastModifiedById, LastModifiedDate, OwnerId, PSG_Owner__c, Pricing_Models__c, Id, System_ID__c, SystemModstamp, VC_Development_Progress__c, VC_Go_Date__c, Venere_Connect__c FROM Connectivity_System__c")

##RecordType
allQueries.append("SELECT IsActive, BusinessProcessId, CreatedById, CreatedDate, Description, LastModifiedById, LastModifiedDate, Name, NamespacePrefix, Id, DeveloperName, SobjectType, SystemModstamp FROM RecordType")

##User
allQueries.append("SELECT AboutMe, AccountId, IsActive, UserPreferencesActivityRemindersPopup, ReceivesAdminInfoEmails, Administration_Notes__c, Alias, ForecastEnabled, UserPermissionsMobileUser, UserPreferencesApexPagesDeveloperMode, Assignment_Group_Active__c, UserPermissionsCallCenterAutoLogin, UserPermissionsAvantgoUser, CallCenterId, MobilePhone, City, CommunityNickname, CompanyName, ContactId, Country, CreatedById, CreatedDate, CurrentStatus, DelegatedApproverId, Department, UserPreferencesDisableAutoSubForFeeds, Division, Email, EmailEncodingKey, EmployeeNumber, Employment_Status__c, UserPreferencesEventRemindersCheckboxDefault, Extended_Leave__c, Extension, Fax, FirstName, Name, ReceivesInfoEmails, LanguageLocaleKey, LastLoginDate, LastModifiedById, LastModifiedDate, LastName, LastPasswordChangeDate, LocaleSidKey, ManagerId, UserPermissionsMarketingUser, Next_Week__c, Office_Location__c, OfflineTrialExpirationDate, UserPermissionsOfflineUser, Phone, ProfileId, UserPreferencesReminderSoundOff, UserRoleId, FederationIdentifier, OfflinePdaTrialExpirationDate, UserPermissionsSFContentUser, State, Street, SystemModstamp, UserPreferencesTaskRemindersCheckboxDefault, Team__c, TimeZoneSidKey, Title, Id, User_Reports_To__c, UserType, Username, PostalCode FROM User")

##EmailMessage
allQueries.append("SELECT ActivityId, BccAddress, CcAddress, ParentId, CreatedById, CreatedDate, IsDeleted, Id, FromAddress, FromName, HtmlBody, HasAttachment, Headers, Incoming, LastModifiedById, LastModifiedDate, MessageDate, Status, Subject, SystemModstamp, TextBody, ToAddress FROM EmailMessage")

sObject = None

def getSalesforceSessionID():
	## Logging in using the Salesforce-Python-SOAP-Toolkit
	## TODO Figure out oauth2
	username, password, securitytoken = getCredentials()
	h = SforceEnterpriseClient('wsdl.jsp.xml')
	h.login(username, password, securitytoken)
	return h.getSessionId()

def getCredentials():
	parser = SafeConfigParser()
	parser.read('sfdc_credentials')
	username = parser.get('sfdc_production', 'USERNAME')
	password = parser.get('sfdc_production', 'PASSWORD')
	securitytoken = parser.get('sfdc_production', 'SECURITY_TOKEN')
	return username, password, securitytoken

def createBulkJob(myQuery):
	#print 'INSIDE CREATE BULK JOB'
	sObject = getSobject(myQuery)
	mySessionId = getSalesforceSessionID()
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	request = urllib2.Request('https://'+instanceURL+'.salesforce.com/services/async/23.0/job')
	request.add_header('X-SFDC-Session: ', mySessionId)
	request.add_header('Content-Type', 'application/xml; charset=UTF-8')
	request.add_data('<?xml version="1.0" encoding="UTF-8"?><jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload"><operation>query</operation><object>'+sObject+'</object> <concurrencyMode>Parallel</concurrencyMode><contentType>CSV</contentType></jobInfo>')
	#request.get_method = lambda: getMethod
	response = opener.open(request).read()
	#print response
	dom = parseString(response)
	xmlTag = dom.getElementsByTagName('id')[0].toxml()
	jobId = xmlTag.replace('<id>', '').replace('</id>', '')
	#print 'The Tag is: ', xmlTag
	#print 'The jobId is:', jobId
	return jobId
	
def doBulkJob(myQuery, jobId):
	#print 'INSIDE DOBULKJOB'
	mySessionId = getSalesforceSessionID()
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	request = urllib2.Request('https://'+instanceURL+'.salesforce.com/services/async/23.0/job/'+jobId+'/batch')
	request.add_header('X-SFDC-Session: ', mySessionId)
	request.add_header('Content-Type', 'text/csv; charset=UTF-8')
	request.add_data(myQuery)
	#request.get_method = lambda: getMethod
	response = opener.open(request).read()
	dom = parseString(response)
	xmlTag = dom.getElementsByTagName('id')[0].toxml()
	batchId = xmlTag.replace('<id>', '').replace('</id>', '')
	#print 'The Tag is: ', xmlTag
	#print 'The batchId is:', batchId

	jobStatus = dom.getElementsByTagName('state')[0].toxml()
	jobStatus = jobStatus.replace('<state>', '').replace('</state>', '')
	#print 'jobstatus: ', jobStatus
	return batchId

def getBulkJobStatus(jobId, batchId):
	mySessionId = getSalesforceSessionID()
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	request = urllib2.Request('https://'+instanceURL+'.salesforce.com/services/async/23.0/job/'+jobId+'/batch/'+batchId)
	request.add_header('X-SFDC-Session: ', mySessionId)
	response = opener.open(request).read()
	#print 'BULKJOBSTATUS', response
	dom = parseString(response)
	jobStatus = dom.getElementsByTagName('state')[0].toxml()
	jobStatus = jobStatus.replace('<state>', '').replace('</state>', '')
	#print 'jobstatus: ', jobStatus
	return jobStatus

def getSobject(query):
	query = query.lower()
	objectStart = query.find('from ') + 5
	objectEnd = query.find(' ', objectStart)
	if objectEnd == -1:
		objectEnd = None
	else:
		objectEnd = objectEnd + 1
	return query[objectStart:objectEnd].strip()
	
	
def getBulkJob(jobId, batchId, myQuery):
	#print 'INSIDE'
	mySessionId = getSalesforceSessionID()
	#print 'session ', mySessionId
	#print 'job ', jobId
	#print 'batch ', batchId
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	request = urllib2.Request('https://'+instanceURL+'.salesforce.com/services/async/23.0/job/'+jobId+'/batch/'+batchId+'/result')
	request.add_header('X-SFDC-Session: ', mySessionId)
	#request.get_method = lambda: getMethod
	response = opener.open(request).read()
	#print response
	
	thisStatus = getBulkJobStatus(jobId, batchId)

	while thisStatus != 'Completed':
		print thisStatus
		thisStatus = getBulkJobStatus(jobId, batchId)
		
	request = urllib2.Request('https://'+instanceURL+'.salesforce.com/services/async/23.0/job/'+jobId+'/batch/'+batchId+'/result')
	request.add_header('X-SFDC-Session: ', mySessionId)
	response = opener.open(request).read()
	#print response	
	dom = parseString(response)
	xmlTag = dom.getElementsByTagName('result')[0].toxml()
	resultId = xmlTag.replace('<result>', '').replace('</result>', '')
	#print 'The Tag is: ', xmlTag
	#print 'The ResultId is:', resultId	
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	request = urllib2.Request('https://'+instanceURL+'.salesforce.com/services/async/23.0/job/'+jobId+'/batch/'+batchId+'/result/'+resultId)
	request.add_header('X-SFDC-Session: ', mySessionId)
	#request.get_method = lambda: getMethod
	response = opener.open(request).read()
	#print 'THE RESULTS ARE IN'
	#print response
	tableName = getSobject(myQuery)
	fileName = tableName + '.csv'
	output = open(fileName, 'w')
	output.write(response)
	output.close()
	print 'FILE ' + fileName +' CREATED'

def closeJob(jobId):
	mySessionId = getSalesforceSessionID()
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	request = urllib2.Request('https://'+instanceURL+'.salesforce.com/services/async/23.0/job/'+jobId)
	request.add_header('X-SFDC-Session: ', mySessionId)
	request.add_header('Content-Type', 'application/xml; charset=UTF-8')
	request.add_data('<?xml version="1.0" encoding="UTF-8"?><jobInfo xmlns="http://www.force.com/2009/06/asyncapi/dataload"><state>Closed</state></jobInfo>')
	response = opener.open(request).read()
	print 'JOB CLOSED'

def Main():
	#myQuery = str(raw_input('Enter Query: '))
	for myQuery in allQueries:
		myQuery = myQuery + ' LIMIT 1000'
		jobId = createBulkJob(myQuery)
		batchId = doBulkJob(myQuery, jobId)
		jobStatus = getBulkJob(jobId, batchId, myQuery)
		closeJob(jobId)


if (__name__== '__main__') and (len(sys.argv) == 1):
	Main()

