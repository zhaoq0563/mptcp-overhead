#!/bin/bash

sudo ovs-ofctl add-flow s3 in_port=2,actions=output:1
sudo ovs-ofctl add-flow s3 in_port=3,actions=output:1
sudo ovs-ofctl add-flow s3 in_port=1,actions=normal
sudo ovs-ofctl add-flow s3 priority=100,actions=normal

sudo ovs-ofctl add-flow s1 in_port=2,actions=output:1
sudo ovs-ofctl add-flow s1 in_port=1,actions=normal
sudo ovs-ofctl add-flow s1 priority=100,actions=normal

sudo ovs-ofctl add-flow s2 in_port=2,actions=output:1
sudo ovs-ofctl add-flow s2 in_port=1,actions=normal
sudo ovs-ofctl add-flow s2 priority=100,actions=normal
