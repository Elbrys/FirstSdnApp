#!/usr/bin/env python
"""
DESCRIPTION:
    This is an extremely simple Python application that demonstrates how to use Elbrys ODL as a service - ODL-S (dev.elbrys.com) to
    control endpoint user sessions access to the network.

    This application will connect to one of the switches that you have connected in the ODL-S portal (sdn-developer.elbrys.com)
    and demonstrate blocking and unblocking of network traffic for any device connected to the switch. 

PRE-REQUISITES:
   1.  Python 2.x
   2.  Install python-requests:
        a.  sudo easy_install requests
   3.  Go to dev.elbrys.com and follow the directions there


Mail bug reports and suggestion to : support@elbrys.com
"""

import sys, os, errno  
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
                'scope': {'vnets':[switch]}}
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


def CreateAuthPolicy(authToken, appId,redirectUrl):
    # This calls the  api to create an authenticated
    # policy for the application.  
    # This is the policy that a new endpoint will
    # be given.
    # This policy will:
    #    - allow any packet to pass
    # RETURNS: app identifier
    # Now create authenticated policy using network resource
    url = odlsBaseUrl + '/applications/' + appId + '/policies'
    payload = {
               'name': 'authenticated',
               'default': True,
               'rules': [
                         {
                          'actions': [
                                        {'type': 'pass'}
                                     ]
                         }
                        ]
              }
    headers = {'content-type': 'application/json',
               'Authorization': 'bearer ' + authToken}
    policyId = requests.post(url, data=json.dumps(payload), headers=headers)
    status = policyId.status_code
    if ((status >= 200) & (status <=299)):
        policyId = policyId.json()
        policyId = policyId['id']
    else:
        print " "
        print "!! Error !!"  
        print "    Unable to create authenticated policy."
        sys.exit()

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
    parser.add_argument('--id',required=True,
        help='your ODL-S Application id.  Go to sdn-developer.elbrys.com, logon, select "My Account" in top right.')
    parser.add_argument('--secret',required=True,
        help='your ODL-S Application secret. Go to sdn-developer.elbrys.com, logon, select "My Account", select "Edit Account", select the "eyeball" icon next to password.')
    parser.add_argument('--switch',required=True,
        help='the Local MAC address for the switch connected in ODL-S dashboard without ":" e.g.  ccfa00b07b95  Go to sdn-developer.elbrys.com, logon, look in "Devices" table')
    return parser
 
def main(): 
    # The version of the application
    version="1.0"
    redirectUrl = "http://sdn-app4-staging.elbrys.com/portal/dan/1/"
    print "ODL-S App1"
    print "Version: " + version
    print "A very simple 'hello world' application that uses ODL-S."
    print __doc__

    # --------------------------------
    #    Command Line Processing
    parser=GetCommandLineParser()
    args = parser.parse_args()

    # --------------------------------
    #    Main application
    print "Obtaining authorization token..."
    authToken = GetAuthToken(args.id,args.secret,parser)
    if (authToken):
        print "...authorization token obtained:" + authToken
        print 'Creating application...'
        appId = CreateApp(authToken, args.switch,parser)
        if (appId):
            try:
                print "...application created with id:" + appId + ".  Now that an application is connected to your "
                print "switch traffic of connected user devices will be blocked until a policy is defined."
                print "Connect a user device (laptop, tablet, phone) to a port on your network device."
                raw_input("Press Enter when you have connected a user device.")
                print "From your user device prove to yourself you do NOT have connectivity.  Ping something."
                raw_input("Press Enter when you have proven your user device is blocked.")
                print "Creating authenticated policy as default for any device detected..."
                authPolicyId = CreateAuthPolicy(authToken, appId,redirectUrl)
                print "...authenticated policy created with id:" + authPolicyId
                print "From your user device prove to yourself you now DO have connectivity.  Try to ping something."
                raw_input("Press Enter when you have proven connectivity to yourself.")
            except:
                print " "
            finally:
                print "Deleting application..."
                DeleteApp(authToken, appId)
                print "...application deleted.  Once the application is deleted you will continue to have connectivity."

 
# The BASE url where the ODL-S RESTful api listens
odlsBaseUrl = "http://app.elbrys.com:8080/ape/v1";

if __name__ == "__main__": 
  main()
