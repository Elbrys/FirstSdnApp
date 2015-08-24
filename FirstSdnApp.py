#!/usr/bin/env python
"""
DESCRIPTION:
    This is an extremely simple Python application that demonstrates how to
     use Elbrys ODL as a service - ODL-S (dev.elbrys.com) to
    control endpoint user sessions access to the network.

    This application will connect to one of the switches that you have
    connected in the ODL-S portal (sdn-developer.elbrys.com)
    and demonstrate blocking and unblocking of network traffic for any device
    connected to the switch.

PRE-REQUISITES:
   1.  Python 2.x
   2.  Install python-requests:
        a.  sudo easy_install requests
   3.  Go to dev.elbrys.com and follow the directions there


Mail bug reports and suggestion to : support@elbrys.com
"""

import sys
import requests
import json
import argparse
from requests.auth import HTTPBasicAuth


def GetAuthToken(user, password, parser):
    global odlsBaseUrl
    # This calls the  api to create an authorization token to make other calls
    # RETURNS: authorization token
    url = odlsBaseUrl + '/auth/token'
    headers = {'content-type': 'application/json'}
    user = "name=" + user
    appId = requests.get(url, headers=headers, auth=HTTPBasicAuth(user,
                         password))
    status = appId.status_code
    if ((status >= 200) & (status <= 299)):
        authToken = appId.json()
        authToken = authToken['token']
    else:
        print " "
        print "!! Error !!"
        print "    Unable to create authorization token.  Double check that\
                   the username and password you entered."
        print "    See usage below:"
        parser.print_help()
        sys.exit()

    return authToken


def GetApps(authToken):
    global odlsBaseUrl
    url = odlsBaseUrl + '/applications'
    headers = {'content-type': 'application/json',
               'Authorization': 'bearer ' + authToken}
    r = requests.get(url, headers=headers)
    if ((r.status_code < 200) | (r.status_code > 299)):
        print "Error getting applications list: " + r.text
        sys.exit()
    else:
        return r


def GetAppInfo(authToken, appId):
    global odlsBaseUrl
    url = odlsBaseUrl + '/applications/' + appId
    headers = {'content-type': 'application/json',
               'Authorization': 'bearer ' + authToken}
    r = requests.get(url, headers=headers)
    if ((r.status_code < 200) | (r.status_code > 299)):
        print "Error getting application info: " + r.text
        sys.exit()
    else:
        return r


def RemoveZombieApps(authToken, switch):
    # Removes any old applications currently connected to the target
    # switch.  Only
    # one application may be connected to a switch.
    apps = GetApps(authToken)
    for a in apps.json():
        appInfo = GetAppInfo(authToken, a['id'])
        appInfo = appInfo.json()
        appScope = appInfo['scope']
        appVnets = appScope['vnets']
        for v in appVnets:
            if (v == switch):
                print "Deleting a zombie application: " + a['id'] + ", "\
                      + a['name']
                DeleteApp(authToken, a['id'])
                break


def CreateApp(authToken, switch, parser):
    global odlsBaseUrl
    # This calls the  api to create an application
    # RETURNS: app identifier
    RemoveZombieApps(authToken, switch)

    url = odlsBaseUrl + '/applications'
    payload = {'name': 'FirstSdnApp/App1 - Example ODL-S for switch: '
               + switch,
               'scope': {'vnets': [switch]}}
    headers = {'content-type': 'application/json',
               'Authorization': 'bearer ' + authToken}
    appId = requests.post(url, data=json.dumps(payload), headers=headers)
    status = appId.status_code
    if ((status >= 200) & (status <= 299)):
        appId = appId.json()
        appId = appId['id']
    else:
        print " "
        print "!! Error !!"
        print "    Unable to create application.  Double check your switch\
                   identifier."
        print "    See usage below:"
        parser.print_help()
        sys.exit()
    return appId


def CreateUnblockPolicy(authToken, appId):
    global odlsBaseUrl
    # This calls the  api to create an authenticated
    # policy for the application.
    # This is the policy that a new endpoint will
    # be given.
    # This policy will:
    #    - allow any packet to pass
    # RETURNS: app identifier
    # Now create authenticated policy using network resource
    url = odlsBaseUrl + '/applications/' + appId + '/policies'
    payload = {'name': 'unblocked',
               'default': True,
               'rules':
               [
                   {'actions':
                    [
                        {'type': 'pass'}]}]}
    headers = {'content-type': 'application/json',
               'Authorization': 'bearer ' + authToken}

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    # print "here 5" + r.status_code
    status = r.status_code
    if ((status >= 200) & (status <= 299)):
        policyId = r.json()
        policyId = policyId['id']
    else:
        print " "
        print "!! Error !!"
        print "    Unable to create unblock policy."
        sys.exit()
    return policyId


def DeleteApp(authToken, appId):
    global odlsBaseUrl
    # This calls the  api to delete an application
    # RETURNS: app identifier
    url = odlsBaseUrl + '/applications/' + appId
    headers = {'content-type': 'application/json',
               'Authorization': 'bearer ' + authToken}
    requests.delete(url, headers=headers)


def RConfGetTopology(rConfBaseUrl, user, password):
    # This calls the RESTConf api to retrieve the topology
    # INPUT:
    #    rConfBaseUrl - base url at which RestConf calls may be
    #           made - example:  http://192.168.56.101:8181/restconf
    #    user - the user name with which to authenticate - example: admin
    #    password - the password with which to authenticate - example - admin
    # RETURNS: topology as JSON
    url = rConfBaseUrl + '/operational/network-topology:network-topology/'

    headers = {'content-type': 'application/json',
               'accept': 'application/json'}
    r = requests.get(url, headers=headers, auth=HTTPBasicAuth(user, password))
    topo = r.json()
    return topo


def AddFlows(rConfBaseUrl, user, password, switchId, flowId, hostMac):
    # Adds two (2) flows with flowId and flowId+1 to switch switchId that
    # has priority of 100
    # that will flood all  packets from or to host with hostMac
    # INPUT:
    #    rConfBaseUrl - base url at which RestConf calls may be
    #    made - example:  http://192.168.56.101:8181/restconf
    #    user - the user name with which to authenticate - example: admin
    #    password - the password with which to authenticate - example - admin
    #    switchId - the id of the switch on which to program the flow.
    #    This is from topology. - example - openflow:1
    #    flowId - the number of the flow to program.  example - 10
    #    hostMac - the MAC address of the host for which to program
    #    flows - example - 46:67:3b:09:61:c7
    # RETURNS: nothing
    print "Adding flows, switchId " \
          + switchId + ", flowId: " + str(flowId) + ", hostMac: " + hostMac
    url = rConfBaseUrl + '/config/opendaylight-inventory:nodes/node/' \
        + switchId + '/table/0/flow/' + str(flowId)

    headers = {'content-type': 'application/json',
               'accept': 'application/json'}

    payload = '{"flow": \
    {"id":"' + str(flowId) + '",\
     "instructions": {"instruction": [\
          {"order": 0,"apply-actions": {"action": [\
                                        {"order": 0,"output-action": \
                                        {"max-length": 65535,\
                                        "output-node-connector": "FLOOD"\
                                        }}]}}]},\
      "match": {"ethernet-match": {"ethernet-source": \
      {"address": "' + hostMac + '"}}},\
      "priority": 100,"table_id": 0,"hard-timeout": 0,"idle-timeout": 0} }'

    r = requests.put(url, data=payload, headers=headers,
                     auth=HTTPBasicAuth(user, password))
    print r.text

    flowId = flowId + 1
    url = rConfBaseUrl + '/config/opendaylight-inventory:nodes/node/' \
        + switchId + '/table/0/flow/' + str(flowId)
    payload = '{"flow": \
    {"id":"' + str(flowId) + '",\
     "instructions": {"instruction": [\
          {"order": 0,"apply-actions": {"action": [\
                                        {"order": 0,"output-action": \
                                        {"max-length": 65535,\
                                        "output-node-connector": "FLOOD"\
                                        }}]}}]},\
      "match": {"ethernet-match": {"ethernet-destination": \
      {"address": "' + hostMac + '"}}},\
      "priority": 100,"table_id": 0,"hard-timeout": 0,"idle-timeout": 0} }'

    r = requests.put(url, data=payload, headers=headers,
                     auth=HTTPBasicAuth(user, password))
    print r.text


def UpdateForwardingRules(rConfBaseUrl, user, password, topology):
    # Evaluates the topology and for each switch adds flows for
    #  each host.  The flows will flood packts to/from the host
    # INPUT:
    #    rConfBaseUrl - base url at which RestConf calls may be
    #    made - example:  http://192.168.56.101:8181/restconf
    #    user - the user name with which to authenticate - example: admin
    #    password - the password with which to authenticate - example - admin
    #    topology - the topology, in JSON, returned from RESTConf get topology
    # RETURNS: nothing

    print "Updating forwarding rules..."

    hosts = []
    switches = []

    if ('network-topology' not in topology):
        print "....no topology."
        return
    else:
        net = topology['network-topology']
        net = net['topology']

        for topo in net:
            if 'node' in topo:
                nodes = topo['node']
                for node in nodes:
                    node_id = node['node-id']
                    if 'host:' in node_id:
                        host = node_id.replace("host:", "", 1)
                        print "new host: " + host
                        hosts.append(host)
                    else:
                        switch = node_id
                        print "new switch: " + switch
                        switches.append(switch)
    flowId = 10
    for host in hosts:
        for switch in switches:
            AddFlows(rConfBaseUrl, user, password, switch, flowId, host)
        flowId = flowId + 5


def PrintTopology(topology):
    # Prints out provided topology.  It is indented 12 spaces.
    # INPUT:
    #    topology - the topology, in JSON, returned from RESTConf get topology
    # RETURNS: nothing

    print "            ======================================================"
    print "            Topology"
    print "            ======================================================"

    if ('network-topology' not in topology):
        print "            No toplogy."
    else:
        net = topology['network-topology']
        net = net['topology']

        for topo in net:
            topo_id = topo['topology-id']
            print "            Network: " + topo_id
            if 'node' in topo:
                nodes = topo['node']
                for node in nodes:
                    node_id = node['node-id']
                    print "                Node: " + node_id
                    if 'termination-point' in node:
                        ports = node['termination-point']
                        for port in ports:
                            port_id = port['tp-id']
                            print "                    Port: " + port_id

    print "            ======================================================"


def opennac_main(args, parser):
    print " "
    print "Obtaining authorization token..."
    authToken = GetAuthToken(args.id, args.secret, parser)
    if (authToken):
        print "...authorization token obtained:" + authToken
        print " "
        print 'Creating application...'
        appId = CreateApp(authToken, args.switch, parser)
        if (appId):
            try:
                print "...application created with id:" + appId
                print " "
                print "Now that an application is connected to your "
                print " switch any traffic to/from connected user devices \
will be blocked until a policy is defined.  Also, you can go to your \
ODL-S dashboard (sdn-developer.elbrys.com) and refresh the screen \
you will see this application listed in the applications table. \n \
Connect a user device (laptop, tablet, phone) to a port on your network \
device. \n"
                raw_input("Press Enter when you have connected a user device.")
                print " \n"
                print "From your user device prove to yourself you do NOT \
have connectivity.  Ping something."
                print " "
                raw_input("Press Enter when you have proven your user \
device is blocked.")
                print " "
                print "Creating unblock policy as default for any device \
detected..."
                unblockPolicyId = CreateUnblockPolicy(authToken, appId)
                print "...unblock policy created with id:" + unblockPolicyId
                print " "
                print "From your user device prove to yourself you now DO \
have connectivity.  Try to ping something."
                print " "
                raw_input("Press Enter to end this application.")
            except Exception as inst:
                print " Exception detected..."
                print type(inst)        # the exception instance
                print inst.args         # arguments stored in .args
                # __str__ allows args to be\
                # printed directly
                print inst
            finally:
                print "Deleting application..."
                DeleteApp(authToken, appId)
                print "...application deleted."
                print ""
                print "Now that the application is deleted you will continue \
to have connectivity. \n If you go to your ODL-S dashboard \
(sdn-developer.elbrys.com) and refresh the screen you will \
no longer see this application listed."


def restconf_main(args):
    global odlsBaseRestConfUrl
    topology = RConfGetTopology(odlsBaseRestConfUrl, args.id, args.secret)
    UpdateForwardingRules(odlsBaseRestConfUrl, args.id, args.secret, topology)
    print "    Initial Topology: "
    PrintTopology(topology)


def GetCommandLineParser():
    # This method will process the command line parameters
    parser = argparse.ArgumentParser(
        description='Simple SDN Application to block/unblock devices connected\
                     to switch.')
    parser.add_argument('--id',
                        required=True,
                        help='your ODL-S Application id.  Go to sdn-developer.\
                        elbrys.com, logon, select "My Account" in top right.')
    parser.add_argument('--secret',
                        required=True,
                        help='your ODL-S Application secret. Go to\
                              sdn-developer.elbrys.com, logon, select "My\
                              Account", select "Edit Account", select the\
                              "eyeball" icon next to password.')
    parser.add_argument('--switch',
                        required=True,
                        help='the Datapath Id (DPID) for the switch connected \
                              in ODL-S dashboard without ":" e.g. \
                              ccfa00b07b95  Go to sdn-developer.elbrys.com, \
                              logon, look in "Devices" table')
    parser.add_argument('--server',
                        required=True,
                        help='The IP address of your ODL-S server.  Go to \
                              sdn-developer.elbrys.com, logon, look at \
                              "Controller" table.')
    parser.add_argument('--port',
                        required=True,
                        help='The TCP port number of your ODL-S server.  \
                              Go to sdn-developer.elbrys.com, logon, look at \
                              "Controller" table.')
    parser.add_argument('--api',
                        required=True,
                        help='The controller northbound api you want to \
                              test. \n\n \
                              restconf - OpenDaylight RESTCONF api. \n \
                              opennac - Elbrys OpenNac api.')
    return parser


def main():
    global odlsBaseUrl
    global odlsBaseOpenNacUrl
    global odlsBaseRestConfUrl
    # The version of the application
    # 1.0 - initial version
    # 1.1 - added code to remove apps for selected vnet before creating new app
    version = "1.1.3"
    print "Elbrys Developer Portal FirstSdnApp"
    print "Version: " + version
    print "A very simple that uses Elbrys' Developer Portal."
    print __doc__

    # --------------------------------
    #    Command Line Processing
    parser = GetCommandLineParser()
    args = parser.parse_args()

    odlsBaseUrl = "http://" + args.server + ":" + args.port
    odlsBaseOpenNacUrl = odlsBaseUrl + "/ape/v1"
    odlsBaseRestConfUrl = odlsBaseUrl + "/restconf"

    print "Elbrys Developer Portal API is at: " + odlsBaseUrl
    print "Elbrys Developer Portal OpenNAC API is at: " + odlsBaseOpenNacUrl
    print "Elbrys Developer Portal RESTCONF API is at: " + odlsBaseRestConfUrl

    if (args.api == 'restconf'):
        restconf_main(args)
    elif (args.api == 'opennac'):
        opennac_main(args, parser)

# The BASE url where the Elbrys' SDN Developer Portal api listens
odlsBaseUrl = None
odlsBaseOpenNacUrl = None
odlsBaseRestConfUrl = None

if __name__ == "__main__":
    main()
