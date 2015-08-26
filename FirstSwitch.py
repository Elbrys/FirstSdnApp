#!/usr/bin/python

from mininet.net import Mininet
# from mininet.node import Controller, RemoteController, OVSController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info
from mininet.node import OVSKernelSwitch, RemoteController
# from mininet.node import UserSwitch
import argparse
import random
import re


def myNetwork(d, server, port):

    net = Mininet(topo=None,
                  build=False)

    info('*** Adding controller\n')
    net.addController(name='c0', controller=RemoteController, ip=server,
                           port=port)

    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, dpid=d)
    Intf('eth1', node=s1)

    info('*** Add hosts\n')
    h1 = net.addHost('h1', ip='0.0.0.0')
    h2 = net.addHost('h2', ip='0.0.0.0')

    info('*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    info('*** Starting network\n')
    net.start()
    h1.cmdPrint('dhclient ' + h1.defaultIntf().name)
    h2.cmdPrint('dhclient ' + h2.defaultIntf().name)
    print " "
    print "If your application is using OpenDaylight RESTCONF api then \
you are ready to go.  Go write your app.\n\n\
If your application will use the Elbrys OpenNAC API then \
this is the data for adding the mininet switch to the list of network \
devices in the ODL-S dashboard (sdn-developer.elbrys.com):"
    print "    Local MAC: " + re.sub("(.{2})", "\\1:", d, 5, re.DOTALL)
    ip = s1.cmd('ifconfig eth0 | grep \'inet addr\' | cut -d: -f2\
                 | awk \'{print $1}\'')
    print "    Local IPv4 Address: " + ip
    dpidAsInt = int(d, 16)
    print "    Datapath id (dpid): " + d + " (decimal: " + str(dpidAsInt) + ")"
    print " "
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')

    parser = argparse.ArgumentParser(description='Simple Mininet application\
     to create and connect Mininet switch to ODL-S.')
    parser.add_argument('--id',
                        required=True,
                        help='your ODL-S Application id.  Go to sdn-developer.\
                        elbrys.com, logon, select "My Account" in top right.')
    parser.add_argument('--server',
                        required=True,
                        help='The IP address of your ODL-S server.  Go to \
                              sdn-developer.elbrys.com, logon, look at \
                              "Controller" table.')
    parser.add_argument('--port',
                        required=True,
                        help='The TCP OpenFlow API port number of your ODL-S \
                          server. Go to sdn-developer.elbrys.com, \
                          logon, look at "Controller" table for \
                          OpenFlow Port.')
    args = parser.parse_args()

    # Create a random dpid that is constant based on input args
    random.seed(args.id)
    r = random.randrange(0x111111111111, 0xffffffffffff)
    r = r | 0x020000000000
    d = format(r, 'x')
    d = str(d)

    # Create the network of switches and endpoints
    myNetwork(d, args.server, int(args.port))
