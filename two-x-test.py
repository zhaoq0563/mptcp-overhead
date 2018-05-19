#!/usr/bin/python

from mininet.fdm_intf_handoff import FDM
from mininet.net import Mininet
from mininet.node import OVSKernelAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

from subprocess import call
import time, random, os
import numpy as np

"""Main function of the simulation"""

def mptcpNet(delay1, delay2, capacity1, capacity2):

    call(["sudo", "sysctl", "-w", "net.mptcp.mptcp_enabled=1"])
    call(["sudo", "modprobe", "mptcp_coupled"])
    call(["sudo", "sysctl", "-w", "net.mptcp.mptcp_scheduler=default"])
    call(["sudo", "sysctl", "-w", "net.ipv4.tcp_congestion_control=lia"])

    net = Mininet(controller=None, accessPoint=OVSKernelAP, link=TCLink, autoSetMacs=True)

    d1 = str(delay1)+'ms'
    d2 = str(delay2)+'ms'
    cap1 = float(capacity1)
    cap2 = float(capacity2)

    print "*** Creating nodes ***"
    '''Host : One host serves as a server'''
    h1 = net.addHost('h1', ip='10.0.0.1')

    '''Switch'''
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    '''Access Point'''

    '''Update the position of each station'''

    '''Station : Defaultly set up the stations with 1 eth and 1 wlan interfaces'''
    sta1 = net.addStation('sta1')

    print "*** Configuring wifi nodes ***"
    net.configureWifiNodes()

    print "*** Associating and Creating links ***"
    '''Backhaul links between switches'''
    net.addLink(h1, s3)
    net.addLink(s3, s1, bw=cap1)
    net.addLink(s3, s2, bw=cap2)

    '''Links between stations and LTE switch'''
    net.addLink(sta1, s1, bw=cap1, delay=d1)
    net.addLink(sta1, s2, bw=cap2, delay=d2)

    print "*** Starting network simulation ***"
    net.start()

    print "*** Addressing for station ***"
    sta1.cmdPrint('ifconfig sta1-eth1 10.0.1.0/32')
    sta1.cmdPrint('ip rule add from 10.0.1.0 table 1')
    sta1.cmdPrint('ip route add 10.0.1.0/32 dev sta1-eth1 scope link table 1')
    sta1.cmdPrint('ip route add default via 10.0.1.0 dev sta1-eth1 table 1')
    sta1.cmdPrint('ip route add default scope global nexthop via 10.0.1.0 dev sta1-eth1')
    sta1.cmdPrint('ifconfig sta1-eth2 10.0.1.1/32')
    sta1.cmdPrint('ip rule add from 10.0.1.1 table 2')
    sta1.cmdPrint('ip route add 10.0.1.1/32 dev sta1-eth2 scope link table 2')
    sta1.cmdPrint('ip route add default via 10.0.1.1 dev sta1-eth2 table 2')
    # sta1.cmdPrint('ip route add default scope global nexthop via 10.0.1.1 dev sta1-eth2')
    sta1.cmdPrint('ifconfig sta1-wlan0 10.0.1.2/32')
    sta1.cmdPrint('ip rule add from 10.0.1.2 table 3')
    sta1.cmdPrint('ip route add 10.0.1.2/32 dev sta1-wlan0 scope link table 3')
    sta1.cmdPrint('ip route add default via 10.0.1.2 dev sta1-wlan0 table 3')

    call(["sudo", "bash", "flowTable.sh"])

    # for i in MPStaSet:
    #     sta_name = 'sta'+str(i)
    #     station = nodes[sta_name]
    #     for j in range(0, wlanPerSta):
    #         station.cmd('ifconfig '+sta_name+'-wlan'+str(j)+' 10.0.'+str(i+1)+'.'+str(j)+'/32')
    #         station.cmd('ip rule add from 10.0.'+str(i+1)+'.'+str(j)+' table '+str(j+1))
    #         station.cmd('ip route add 10.0.'+str(i+1)+'.'+str(j)+'/32 dev '+sta_name+'-wlan'+str(j)+' scope link table '+str(j+1))
    #         station.cmd('ip route add default via 10.0.'+str(i+1)+'.'+str(j)+' dev '+sta_name+'-wlan'+str(j)+' table '+str(j+1))
    #         if j==0:
    #             station.cmd('ip route add default scope global nexthop via 10.0.'+str(i+1)+'.'+str(j)+' dev '+sta_name+'-wlan'+str(j))
    #     for j in range(wlanPerSta, ethPerSta+wlanPerSta):
    #         station.cmd('ifconfig '+sta_name+'-eth'+str(j)+' 10.0.'+str(i+1)+'.'+str(j)+'/32')
    #         station.cmd('ip rule add from 10.0.'+str(i+1)+'.'+str(j)+' table '+str(j+1))
    #         station.cmd('ip route add 10.0.'+str(i+1)+'.'+str(j)+'/32 dev '+sta_name+'-eth'+str(j)+' scope link table '+str(j+1))
    #         station.cmd('ip route add default via 10.0.'+str(i+1)+'.'+str(j)+' dev '+sta_name+'-eth'+str(j)+' table '+str(j+1))
    # for i in range(1, numOfSPSta+numOfMPSta+1):
    #     if i not in MPStaSet:
    #         sta_name = 'sta'+str(i)
    #         station = nodes[sta_name]
    #         station.cmd('ifconfig '+sta_name+'-wlan0 10.0.'+str(i+1)+'.0/32')
    #         station.cmd('ip route add default via 10.0.'+str(i+1)+'.0 dev '+sta_name+'-wlan0')
    # for i in range(numOfSPSta+numOfMPSta+1, numOfSPSta+numOfMPSta+numOfFixApSta+1):
    #     sta_name = 'sta'+str(i)
    #     station = nodes[sta_name]
    #     station.cmd('ifconfig '+sta_name+'-wlan0 10.0.'+str(i+1)+'.0/32')
    #     station.cmd('ip route add default via 10.0.'+str(i+1)+'.0 dev '+sta_name+'-wlan0')
    # for i in range(numOfSPSta+numOfMPSta+numOfFixApSta+1, numOfSPSta+numOfMPSta+numOfFixApSta+numOfFixLteSta+1):
    #     sta_name = 'sta'+str(i)
    #     station = nodes[sta_name]
    #     station.cmd('ifconfig '+sta_name+'-eth1 10.0.'+str(i+1)+'.1/32')
    #     station.cmd('ifconfig '+sta_name +'-wlan0 10.0.'+str(i+1)+'.0/32')
    #     station.cmd('ip route add default scope global nexthop via 10.0.'+str(i+1)+'.1 dev '+station.name+'-eth1')


    print "***Running CLI"
    # CLI(net)

    print "*** Starting to generate the traffic ***"
    info('Starting iPerf3 server...\n')
    folderName = 'bs'
    h1.cmdPrint('iperf3 -s &')
    # h1.cmdPrint('PID=$!')
    if not os.path.exists(folderName):
        os.mkdir(folderName)
        user = os.getenv('SUDO_USER')
        os.system('sudo chown -R ' + user + ':' + user + ' ' + folderName)
    h1.cmd('tcpdump -i h1-eth0 -w ' + folderName + '/h1.pcap &')

    print "*** Starting iPerf3 Clients on stations ***"
    info('Sending iperf3 from sta1<->h1...\n')
    time.sleep(1)
    sta1.cmdPrint('iperf3 -c 10.0.0.1 -t 19 &')
    # sta1.cmdPrint('PID=$!')
    # sta1.cmdPrint('ifstat -b &')
    sta1.cmd('tcpdump -i sta1-eth1 -w '+ folderName + '/sta1-eth1.pcap &')
    sta1.cmd('tcpdump -i sta1-eth2 -w '+ folderName + '/sta1-eth2.pcap &')

    print "*** Simulation is running. Please wait... ***"
    time.sleep(19)

    print "*** Stopping traffic generator on host ***"
    # h1.cmd('kill $PID')

    print "*** Data processing ***"
    # throughput_l = []
    # delay_l = []
    throughput, delay, byte = (0.0, 0.0, 0.0)
    out_f = folderName + '/sta1-eht1.stat'
    h1.cmd('sudo tshark -r ' + folderName + '/sta1-eth1.pcap -qz \"io,stat,0,BYTES()ip.src==10.0.1.0,AVG(tcp.analysis.ack_rtt)tcp.analysis.ack_rtt&&ip.addr==10.0.1.0\" >' + out_f)
    f = open(out_f, 'r')
    for line in f:
        if line.startswith('|'):
            l = line.strip().strip('|').split()
            if '<>' in l:
                duration = float(l[2])
                byte += float(l[8])
                throughput += float(l[8]) * 8 / duration
                delay += float(l[8]) * float(l[10])
    f.close()
    out_f = folderName + '/sta1-eht2.stat'
    h1.cmd('sudo tshark -r ' + folderName + '/sta1-eth2.pcap -qz \"io,stat,0,BYTES()ip.src==10.0.1.1,AVG(tcp.analysis.ack_rtt)tcp.analysis.ack_rtt&&ip.addr==10.0.1.1\" >' + out_f)
    f = open(out_f, 'r')
    for line in f:
        if line.startswith('|'):
            l = line.strip().strip('|').split()
            if '<>' in l:
                duration = float(l[2])
                byte += float(l[8])
                throughput += float(l[8]) * 8 / duration
                delay += float(l[8]) * float(l[10])
    f.close()
    delay /= byte
    # throughput_l.append(str(throughput))
    # delay_l.append(str(delay))
    # out_f = folderName + '/sta1-wireshark.stat'
    # o = open(out_f, 'w')
    # o.write(str(throughput) + "\n" + str(delay))
    # o.close()

    r = open('reg-data/x-y.stat','a')
    r1 = open('reg-data/throughput.stat','a')
    r2 = open('reg-data/delay.stat','a')
    r3 = open('reg-data/throughput-ratio.stat', 'a')
    x_y = [float(delay2/delay1), float(capacity2/capacity1)]
    r.write(','.join(str(i) for i in x_y))
    r.write('\n')
    r1.write(str(throughput)+',')
    r2.write(str(delay)+',')
    if capacity2>=capacity1:
        ratio = float(throughput/10**6)/capacity2
    r3.write(str(ratio)+',')
    r.close()
    r1.close()
    r2.close()
    r3.close()

    os.system('rm -rf '+folderName)

    print "*** Stopping network ***"
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    delay = list(np.arange(1,500,1))
    print delay
    delay1 = 1

    capacity = [0.1, 0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0]
    capacity1 = 1.0

    for i in delay:
        delay2 = int(i)
        for j in capacity:
            capacity2 = float(j)
            mptcpNet(delay1, delay2, capacity1, capacity2)
    # mptcpNet('1ms', '1ms')