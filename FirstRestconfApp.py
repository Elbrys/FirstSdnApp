#!/usr/bin/env python
"""
DESCRIPTION:
    This is an extremely simple Python application that demonstrates how to
     use Elbrys ODL as a service - ODL-S (dev.elbrys.com) to
    control endpoint user sessions access to the network.

    This application will use the RESTCONF api to obtain the networks
    topology and print it out.

PRE-REQUISITES:
   1.  Python 2.x
   2.  Install python-requests:
        a.  sudo easy_install requests
   3.  Go to dev.elbrys.com and follow the directions there


Mail bug reports and suggestion to : support@elbrys.com
"""

import requests
import argparse
from requests.auth import HTTPBasicAuth


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
    parser.add_argument('--server',
                        required=True,
                        help='The IP address of your ODL-S server.  Go to \
                              sdn-developer.elbrys.com, logon, look at \
                              "Controller" table.')
    parser.add_argument('--port',
                        required=True,
                        help='The TCP REST API port number of your ODL-S \
                              server. Go to sdn-developer.elbrys.com, \
                              logon, look at "Controller" table for \
                              REST API Port.')
    return parser


def main():
    global odlsBaseUrl
    global odlsBaseRestConfUrl
    # The version of the application
    # 1.0 - initial version
    # 1.1 - added code to remove apps for selected vnet before creating new app
    version = "1.1.3"
    print "Elbrys Developer Portal FirstRestconfApp"
    print "Version: " + version
    print "A very simple that uses RESTCONF api of Elbrys' Developer Portal."
    print __doc__

    # --------------------------------
    #    Command Line Processing
    parser = GetCommandLineParser()
    args = parser.parse_args()

    odlsBaseUrl = "http://" + args.server + ":" + args.port
    odlsBaseRestConfUrl = odlsBaseUrl + "/restconf"

    print "Elbrys Developer Portal API is at: " + odlsBaseUrl
    print "Elbrys Developer Portal RESTCONF API is at: " + odlsBaseRestConfUrl

    topology = RConfGetTopology(odlsBaseRestConfUrl, args.id, args.secret)
    print "    Initial Topology: "
    PrintTopology(topology)

# The BASE url where the Elbrys' SDN Developer Portal api listens
odlsBaseUrl = None
odlsBaseRestConfUrl = None

if __name__ == "__main__":
    main()
