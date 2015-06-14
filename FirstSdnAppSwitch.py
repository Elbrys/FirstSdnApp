#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info
from mininet.node import OVSKernelSwitch, UserSwitch
import argparse
import random
import re

def myNetwork(d):

    net = Mininet( topo=None,
                   build=False)

    info( '*** Adding controller\n' )
    #net.addController(name='c0')
    c1=net.addController(name='c0', controller=RemoteController, ip='54.85.212.52', port=6634)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, dpid=d)
    #s1 = net.addSwitch('s1', cls=OVSKernelSwitch, dpid='1')
    Intf( 'eth2', node=s1 )

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', ip='0.0.0.0')

    info( '*** Add links\n')
    net.addLink(h1, s1)

    info( '*** Starting network\n')
    net.start()
    h1.cmdPrint('dhclient '+h1.defaultIntf().name)
    print " "
    print "Data for adding device to ODL-S dashboard (sdn-developer.elbrys.com):"
    print "    Local MAC: " + re.sub("(.{2})", "\\1:", d, 5, re.DOTALL)
    ip = s1.cmd('ifconfig eth0 | grep \'inet addr\' | cut -d: -f2 | awk \'{print $1}\'')
    print "    Local IPv4 Address: " + ip
    print "    Datapath id (dpid): " + d
    print " "
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )

    parser = argparse.ArgumentParser(description='Simple Mininet application to create and connect Mininet switch to ODL-S.')
    parser.add_argument('--id',required=True,
        help='your ODL-S Application id.  Go to sdn-developer.elbrys.com, logon, select "My Account" in top right.')
    args = parser.parse_args()
    random.seed(args.id)
    r = random.randrange(0x111111111111,0xffffffffffff)
    r = r | 0x020000000000
    d = format(r, 'x')
    d = str(d)
    
    myNetwork(d)