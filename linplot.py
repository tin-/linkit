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

if len(sys.argv) < 3:
    print("Need an argument!\n%s <file_name> <out_fn> [<data_row_number>] [<dut_name>] [<meter_name>]" % sys.argv[0])
    quit()

if len(sys.argv) >= 4:
    real_row = int(sys.argv[3])

if len(sys.argv) >= 5:
    mfc_name = sys.argv[4]

if len(sys.argv) == 6:
    meter_name = sys.argv[5]

fn = sys.argv[1]
out_fn = sys.argv[2]

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

# Print the result as CSV
for i in range(0,len(diff_ppm)):
    print("%0.2f,%f" % (ideal[i],diff_ppm[i]))

fig, ax = plt.subplots()
ax.plot(ideal, diff_ppm)
ax.axis([-10.9, 10.9, -0.5, 0.5])
ax.set(xlabel='Voltage', ylabel='INL ppm 10V',
       title='%s vs %s Linearity' % (mfc_name,meter_name))
ax.grid()
fig.savefig(out_fn)
print("Plot %s generated" % out_fn)
