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
    payload = {'name': 'FirstSdnApp - Example ODL-S for switch: ' + switch,
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


def CreateUnblockPolicy(authToken, appId):
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
               'name': 'unblocked',
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

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    # print "here 5" + r.status_code
    status = r.status_code
    if ((status >= 200) & (status <=299)):
        policyId = r.json()
        policyId = policyId['id']
    else:
        print " "
        print "!! Error !!"  
        print "    Unable to create unblock policy."
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
    parser = argparse.ArgumentParser(description='Simple SDN Application to block/unblock devices connected to switch.')
    parser.add_argument('--id',required=True,
        help='your ODL-S Application id.  Go to sdn-developer.elbrys.com, logon, select "My Account" in top right.')
    parser.add_argument('--secret',required=True,
        help='your ODL-S Application secret. Go to sdn-developer.elbrys.com, logon, select "My Account", select "Edit Account", select the "eyeball" icon next to password.')
    parser.add_argument('--switch',required=True,
        help='the Datapath Id (DPID) for the switch connected in ODL-S dashboard without ":" e.g.  ccfa00b07b95  Go to sdn-developer.elbrys.com, logon, look in "Devices" table')
    return parser
 
def main(): 
    # The version of the application
    version="1.0"
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
    print " "
    print "Obtaining authorization token..."
    authToken = GetAuthToken(args.id,args.secret,parser)
    if (authToken):
        print "...authorization token obtained:" + authToken
        print " "
        print 'Creating application...'
        appId = CreateApp(authToken, args.switch,parser)
        if (appId):
            try:
                print "...application created with id:" + appId 
                print " "
                print "Now that an application is connected to your "
                print " switch any traffic to/from connected user devices will be blocked until a policy is defined."
                print " Also, you can go to your ODL-S dashboard (sdn-developer.elbrys.com) and refresh the screen "
                print " you will see this application listed in the applications table."
                print " "
                print "Connect a user device (laptop, tablet, phone) to a port on your network device."
                print " "
                raw_input("Press Enter when you have connected a user device.")
                print " "
                print "From your user device prove to yourself you do NOT have connectivity.  Ping something."
                print " "
                raw_input("Press Enter when you have proven your user device is blocked.")
                print " "
                print "Creating unblock policy as default for any device detected..."
                unblockPolicyId = CreateUnblockPolicy(authToken, appId)
                print "...unblock policy created with id:" + unblockPolicyId
                print " "
                print "From your user device prove to yourself you now DO have connectivity.  Try to ping something."
                print " "
                raw_input("Press Enter to end this application.")
            except Exception as inst:
                print " Exception detected..."
                print type(inst)     # the exception instance
                print inst.args      # arguments stored in .args
                print inst           # __str__ allows args to be printed directly
            finally:
                print "Deleting application..."
                DeleteApp(authToken, appId)
                print "...application deleted."
                print ""
                print "Now that the application is deleted you will continue to have connectivity."
                print "If you go to your ODL-S dashboard (sdn-developer.elbrys.com) and refresh the screen you will "
                print " no longer see this application listed."

 
# The BASE url where the ODL-S RESTful api listens
odlsBaseUrl = "http://app.elbrys.com:8080/ape/v1";

if __name__ == "__main__": 
  main()

