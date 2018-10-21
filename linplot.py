#!/usr/bin/python
import sys
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv
matplotlib.use('Agg')

mfc_name = "DUT"
meter_name = "3458A"
real_row = 2

if len(sys.argv) < 2:
    print("Need an argument! <file_name> [<data_row_number>] [<dut_name>] [<meter_name>]")
    quit()

if len(sys.argv) >= 3:
    real_row = int(sys.argv[2])

if len(sys.argv) >= 4:
    mfc_name = sys.argv[3]

if len(sys.argv) == 5:
    meter_name = sys.argv[4]

fn = sys.argv[1]

ideal = []
real = []

with open(fn) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    is_first = True
    for row in spamreader:
        if is_first:
            is_first = False
            continue
        ideal.extend([float(row[1])])
        real.extend([float(row[real_row])])

p = np.polyfit(real,ideal,1)
pv = np.polyval(p,real)
diff = ideal-pv
diff_ppm = (diff/10.0)*1000000.0

inl_max = np.amax(diff_ppm)
inl_min = np.amin(diff_ppm)
inl_delta = inl_max - inl_min
inl_span = inl_delta / 2.0

print(mfc_name + " vs " + meter_name + " INL Max: %f, Min %f" % (inl_max , inl_min))
print(mfc_name + " vs " + meter_name + " INL +-%f" % inl_span)

fig, ax = plt.subplots()
ax.plot(ideal, diff_ppm)
ax.axis([-10.9, 10.9, -0.5, 0.5])
ax.set(xlabel='Voltage', ylabel='INL ppm 10V',
       title='%s vs %s Linearity' % (mfc_name,meter_name))
ax.grid()

#plt.show()
fig.savefig("test_hulk.png")
