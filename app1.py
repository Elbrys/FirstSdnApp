#!/usr/bin/env python
"""
DESCRIPTION:
    This is an example Python application that demonstrates how to use Elbrys ODL as a service - ODL-S (dev.elbrys.com) to
    control endpoint user sessions access to the network.

    This application will connect to one of the switches that you have connected in the ODL-S portal (sdn-developer.elbrys.com)
    and redirect all endpoints that connect to the switch to a specific url.

PRE-REQUISITES:
   1.  Python 2.x
   2.  Install python-requests:
        a.  sudo easy_install requests
   3.  Go to dev.elbrys.com and follow the directions there


TRY IT OUT WHILE IT IS RUNNING: 
   1.  Connect a user device (laptop, phone, tablet, etc.) to your switch 
   2.  On the user device, if you are not redirected automatically, open your web browser, browse to a non https url (www.amazon.com).
       You will be redirected to www.elbrys.com.  You should be able to browse to www.elbrys.com
       (this is because the IP address of www.elbrys.com is whitelisted)
 
Mail bug reports and suggestion to : support@elbrys.com
"""

# =================================================================
# Example execution:

# python ./app1.py --user myusername --password mypassword --switch ccfa00b07b95 --unauthwait 120
# EXAMPLE application #1 
# Version: 1.0
# Creating application...
# ...application created with id:1412228378082
# Creating unauthenticated policy as default...
# ...unauthenticated policy created with id:1412228378083
# Waiting 120 seconds for you to associate an endpoint and try default policy. Open browser try to go to a url...
# ...done waiting.
# Deleting application...
# ...application deleted.
# ====================================================================
 
import getopt, sys, os, errno  
import getpass    
import requests
import json
import time
import argparse
from requests.auth import HTTPBasicAuth
 
def GetAuthToken(user, password, parser):
    # This calls the  api to create an authorization token to make other calls
    # RETURNS: authorization token
    url = odlsBaseUrl + '/auth/token'
    headers = {'content-type': 'application/json'}
    user = "name="+user
    appId = requests.get(url, headers=headers, auth=HTTPBasicAuth(user,password))
    result = appId.text
    status = appId.status_code
    if ((status >= 200) & (status <=299)):
        authToken = appId.json()
        authToken = authToken['token']
    else:
        print " "
        print "!! Error !!"  
        print "    Unable to create authorization token.  Double check that the username and password you entered."
        print "    See usage below:"
        parser.print_help()
        sys.exit()

    return authToken;

def CreateApp(authToken, switch, parser):
    # This calls the  api to create an application
    # RETURNS: app identifier
    url = odlsBaseUrl + '/applications'
    payload = {'name': 'Example ODL-S app1.py for switch: ' + switch,
                'scope': {'switchs':[switch]}}
    headers = {'content-type': 'application/json',
               'Authorization': 'bearer ' + authToken}
    appId = requests.post(url, data=json.dumps(payload), headers=headers)
    result = appId.text
    status = appId.status_code
    if ((status >= 200) & (status <=299)):
        appId = appId.json()
        appId = appId['id']
    else:
        print " "
        print "!! Error !!"  
        print "    Unable to create application.  Double check your switch identifier."
        print "    See usage below:"
        parser.print_help()
        sys.exit()

    return appId;


def CreateUnauthPolicy(authToken, appId,redirectUrl):
    # This calls the  api to create an unauthenticated
    # policy for the application.  
    # This is the policy that a new endpoint will
    # be given.
    # This policy will:
    #    - redirect any http requests to redirectUrl 
    # RETURNS: app identifier
    # Now create unauthenticated policy using network resource
    url = odlsBaseUrl + '/applications/' + appId + '/policies'
    payload = {
               'name': 'unauthenticated',
               'default': True,
               'rules': [
                         {
                          'actions': [
                                       {
                                        'type': 'httpRedirect',
                                        'url': redirectUrl
                                        }
                                     ]
                         }
                        ]
              }
    headers = {'content-type': 'application/json',
               'Authorization': 'bearer ' + authToken}
    policyId = requests.post(url, data=json.dumps(payload), headers=headers)
    policyId = policyId.json()
    policyId = policyId['id']
    return policyId;


def DeleteApp(authToken, appId):
    # This calls the  api to delete an application
    # RETURNS: app identifier
    url = odlsBaseUrl + '/applications/' + appId
    headers = {'content-type': 'application/json',
               'Authorization': 'bearer ' + authToken}
    r = requests.delete(url, headers=headers)


def GetCommandLineParser():
    # This method will process the command line parameters
    parser = argparse.ArgumentParser(description='SDN Application to redirect devices connected to switch to a url.')
    parser.add_argument('--wait',type=int,default=120,
        help='the number of seconds the application will pause to allow you to connect end user device to switch to try it out.')
    parser.add_argument('--user',required=True,
        help='your ODL-S Account Username.  Go to sdn-developer.elbrys.com, logon, select "My Account" in top right.')
    parser.add_argument('--password',required=True,
        help='your ODL-S Account Password. Go to sdn-developer.elbrys.com, logon, select "My Account", select "Edit Account", select the "eyeball" icon next to password.')
    parser.add_argument('--switch',required=True,
        help='the Local MAC address for the switch connected in ODL-S dashboard without ":" e.g.  ccfa00b07b95  Go to sdn-developer.elbrys.com, logon, look in "Devices" table')
    return parser
 
def main(): 
    # The version of the application
    version="1.0"
    redirectUrl = "http://sdn-app4-staging.elbrys.com/portal/dan/1/"
    print "ODL-S App1"
    print "Version: " + version
    print __doc__

    # --------------------------------
    #    Command Line Processing
    parser=GetCommandLineParser()
    args = parser.parse_args()

    # --------------------------------
    #    Main application
    print "Obtaining authorization token..."
    authToken = GetAuthToken(args.user,args.password,parser)
    if (authToken):
        print "...authorization token obtained:" + authToken
        print "Creating application..."
        appId = CreateApp(authToken, args.switch,parser)
        if (appId):
            try:
                print "...application created with id:" + appId
                print "Creating unauthenticated policy as default..."
                unAuthPolicyId = CreateUnauthPolicy(authToken, appId,redirectUrl)
                print "...unauthenticated policy created with id:" + unAuthPolicyId
                print "Waiting " + `args.wait` + " seconds for you to associate an endpoint and try default policy. Open browser try to go to a url..."
                time.sleep(args.wait)
                print "...done waiting."
            except:
                print " "
            finally:
                print "Deleting application..."
                DeleteApp(authToken, appId)
                print "...application deleted."

 
# The BASE url where the ODL-S RESTful api listens
odlsBaseUrl = "http://app.elbrys.com:8080/ape/v1";

if __name__ == "__main__": 
  main()

