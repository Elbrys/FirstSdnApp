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
    Intf('eth2', node=s1)

    info('*** Add hosts\n')
    h1 = net.addHost('h1', ip='0.0.0.0')

    info('*** Add links\n')
    net.addLink(h1, s1)

    info('*** Starting network\n')
    net.start()
    h1.cmdPrint('dhclient ' + h1.defaultIntf().name)
    print " "
    print "Data for adding device to ODL-S dashboard (sdn-developer.elbrys.\
           com):"
    print "    Local MAC: " + re.sub("(.{2})", "\\1:", d, 5, re.DOTALL)
    ip = s1.cmd('ifconfig eth0 | grep \'inet addr\' | cut -d: -f2\
                 | awk \'{print $1}\'')
    print "    Local IPv4 Address: " + ip
    print "    Datapath id (dpid): " + d
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
                        help='The TCP port number of your ODL-S server.\
                              Go to sdn-developer.\
                              elbrys.com, logon, look at "Controller" table.')
    args = parser.parse_args()

    # Create a random dpid that is constant based on input args
    random.seed(args.id)
    r = random.randrange(0x111111111111, 0xffffffffffff)
    r = r | 0x020000000000
    d = format(r, 'x')
    d = str(d)

    # Create the network of switches and endpoints
    myNetwork(d, args.server, args.port)
