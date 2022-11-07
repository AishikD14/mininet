"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        h1 = self.addHost( 'h1', ip='192.168.0.100/24', defaultRoute='via 192.168.0.1'  )
        h2 = self.addHost( 'h2', ip='172.16.0.100/24', defaultRoute='via 172.16.0.1'  )
        r1 = self.addNode( 'r1', cls=LinuxRouter, ip="192.168.0.1/24" )
        r2 = self.addNode( 'r2', cls=LinuxRouter, ip="20.0.0.2/24" )
        r3 = self.addNode( 'r3', cls=LinuxRouter, ip="10.0.0.2/24" )
        r4 = self.addNode( 'r4', cls=LinuxRouter, ip="30.0.0.2/24" )

        # Add links
        self.addLink( h1, r1, intfName1='h1-eth0', intfName2='r1-eth0', params1={ 'ip' : "192.168.0.100/24" }, params2={ 'ip' : "192.168.0.1/24" } )
        self.addLink( r1, r2, intfName1='r1-eth1', intfName2='r2-eth1', params1={ 'ip' : "20.0.0.1/24" }, params2={ 'ip' : "20.0.0.2/24" } )
        self.addLink( r1, r3, intfName1='r1-eth2', intfName2='r3-eth2', params1={ 'ip' : "10.0.0.1/24" }, params2={ 'ip' : "10.0.0.2/24" } )
        self.addLink( r2, r4, intfName1='r2-eth4', intfName2='r4-eth4', params1={ 'ip' : "30.0.0.1/24" }, params2={ 'ip' : "30.0.0.2/24" } )
        self.addLink( r3, r4, intfName1='r3-eth3', intfName2='r4-eth3', params1={ 'ip' : "40.0.0.1/24" }, params2={ 'ip' : "40.0.0.2/24" } )
        self.addLink( r4, h2, intfName1='r4-eth5', intfName2='h2-eth5', params1={ 'ip' : "172.16.0.1/24" }, params2={ 'ip' : "172.16.0.100/24" } )

def run():
    topo = MyTopo()
    net = Mininet(topo=topo)

    # Add routing for reaching networks that aren't directly connected
    
    info(net['r1'].cmd("ip route add 30.0.0.0/24 via 20.0.0.2 dev r1-eth1"))
    info(net['r1'].cmd("ip route add 40.0.0.0/24 via 10.0.0.2 dev r1-eth2"))
    info(net['r1'].cmd("ip route add 172.16.0.0/24 via 20.0.0.2 dev r1-eth1"))
    info(net['r1'].cmd("ip route add 172.16.0.0/24 via 10.0.0.2 dev r1-eth2"))
    
    info(net['r2'].cmd("ip route add 40.0.0.0/24 via 30.0.0.2 dev r2-eth4"))
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 20.0.0.1 dev r2-eth1"))
    info(net['r2'].cmd("ip route add 172.16.0.0/24 via 30.0.0.2 dev r2-eth4"))
    info(net['r2'].cmd("ip route add 192.168.0.0/24 via 20.0.0.1 dev r2-eth1"))

    info(net['r3'].cmd("ip route add 172.16.0.0/24 via 40.0.0.2 dev r3-eth3"))
    info(net['r3'].cmd("ip route add 192.168.0.0/24 via 10.0.0.1 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 30.0.0.0/24 via 40.0.0.2 dev r3-eth3"))
    info(net['r3'].cmd("ip route add 20.0.0.0/24 via 10.0.0.1 dev r3-eth2"))
    
    info(net['r4'].cmd("ip route add 20.0.0.0/24 via 30.0.0.1 dev r4-eth4"))
    info(net['r4'].cmd("ip route add 10.0.0.0/24 via 40.0.0.1 dev r4-eth3"))
    info(net['r4'].cmd("ip route add 192.168.0.0/24 via 30.0.0.1 dev r4-eth4"))
    info(net['r4'].cmd("ip route add 192.168.0.0/24 via 40.0.0.1 dev r4-eth3"))

    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()

# topos = { 'mytopo': ( lambda: MyTopo() ) }