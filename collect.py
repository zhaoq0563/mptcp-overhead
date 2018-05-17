#!/usr/bin/python

import os
import numpy as np

os.system('mkdir data')

delay = list(np.arange(5,500,5))
delay.insert(0, 1)

data = './data/data.stat'
f = open(data, 'w')

xl = []
yl = []
zl = []

for i in delay:
	folder = '1ms-'+str(i)+'ms'
	x = float(i/1)
	xl.append(x)
	r = open(folder+'/sta1-wireshark.stat', 'r')
	throughput = float(r.readline().strip('\n'))
	delay = float(r.readline().strip('\n'))
	yl.append(throughput)
	zl.append(delay)
	r.close()

print xl, yl

f.write(','.join(str(i) for i in xl))
f.write('\n')
f.write(','.join(str(i) for i in yl))
f.write('\n')
f.write(','.join(str(i) for i in zl))
f.close