#!/usr/bin/python
# Linearity plot demo app, require matplotlib and Python 3
# Revision 6.1 AUG.5.2024
# xDevs.com LinKIT INL sweeper tool
# (C) Illya Tsemenko

#!/usr/bin/python
import sys
import time
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.ticker as ticker
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import scipy.ndimage.filters
import scipy.interpolate
import configparser                                   # Library to support config file parsing
import os
cwd = os.getcwd()
print(cwd)

cfg = configparser.ConfigParser(inline_comment_prefixes=(';','#',))
cfg.read('linkit2.conf')
cfg.sections()

if (len(sys.argv) <= 1):
    fn = cfg.get('main', 'data_filename')       # Read data input filename from config file
else:
    fn = sys.argv[1]                               # Read data input filename from command line arg

fnout = cwd + "\\" + fn.split(".dsv")[0] + "_sorted.dsv"

chart_name   = cfg.get('plot', 'chart_title')
ref_range1   = float(cfg.get('main', 'reference_value'))
ref_range2   = float(cfg.get('main', 'reference_value2'))
baseline_col = int(cfg.get('main', 'baseline_ref_column'))
axis_y_max   = float(cfg.get('plot', 'y_max'))
axis_y_min   = float(cfg.get('plot', 'y_min'))
axis_y_step  = float(cfg.get('plot', 'y_resolution'))
axis_y_label = cfg.get('plot', 'y_label')
axis_x_max   = float(cfg.get('plot', 'x_max'))
axis_x_min   = float(cfg.get('plot', 'x_min'))
axis_x_step  = float(cfg.get('plot', 'x_resolution'))
axis_x_label = cfg.get('plot', 'x_label')

dataset_name1 = cfg.get('main', 'dataset_name1')
dataset_name2 = cfg.get('main', 'dataset_name2')
dataset_name3 = cfg.get('main', 'dataset_name3')
dataset_name4 = cfg.get('main', 'dataset_name4')
dataset_name5 = cfg.get('main', 'dataset_name5')
dataset_name6 = cfg.get('main', 'dataset_name6')
dataset_name7 = cfg.get('main', 'dataset_name7')
dataset_name8 = cfg.get('main', 'dataset_name8')
dataset_name9 = cfg.get('main', 'dataset_name9')
dataset_name10 = "1σ error" #cfg.get('main', 'dataset_name3')
dataset_name11 = cfg.get('main', 'dataset_name11')
dataset_name12 = cfg.get('main', 'dataset_name12')

dataset_color1  = cfg.get('plot', 'dataset_color1')
dataset_color2  = cfg.get('plot', 'dataset_color2')
dataset_color3  = cfg.get('plot', 'dataset_color3')
dataset_color4  = cfg.get('plot', 'dataset_color4')
dataset_color5  = cfg.get('plot', 'dataset_color5')
dataset_color6  = cfg.get('plot', 'dataset_color6')
dataset_color7  = cfg.get('plot', 'dataset_color7')
dataset_color8  = cfg.get('plot', 'dataset_color8')
dataset_color9  = cfg.get('plot', 'dataset_color9')
dataset_color10 = cfg.get('plot', 'dataset_color10')
dataset_color11 = cfg.get('plot', 'dataset_color11')
dataset_color12 = cfg.get('plot', 'dataset_color12')

# Resort data from input random DSV
df = pd.read_csv(fn , skiprows=0, sep=';', index_col = 0)
print ("-i- Read file into DF [A]")
print ("\033[31;1m", df.head(8))
df_out = df.sort_values(by='source')
print ("\033[31;1m", df_out.head(8))
print (fnout)
df_out.to_csv(fnout, sep=';')# header=None)
    
real_row = 2
idxr = []
cntr = []
ideal = []
ideal2 = []
real = []
real2 = []
real3 = []
real4 = []
real5 = []
real6 = []
real7 = []
real8 = []
real9 = []
chdiff = []
gain1diff = []
gain2diff = []
gainhdiff = []
error1 = []
error2 = []
error3 = []
error4 = []
error5 = []
error6 = []
error7 = []
error8 = []
error9 = []
ambient = []
rh = []
pressure = []
count = 0

print ("INL plot configured to reference col #%d, R1 %.3f R2 %.3f" % (baseline_col, ref_range1, ref_range2))
title_label = 'Sweep DCV, random points, NPLC10, DUT: 2xK2001' #3xHP3458A + K2002 (ale)
axis4_y_label = "Ambient temperature, °C"
axis2_x_label = "Voltage point by triple 3458A, V DC"
stats_units = "µV"
axis2_y_label = ("Standard deviation (self-referenced), %s/V" % stats_units)
axis3_y_label = "Ambient T, "
axis5_y_label = "Deviation error, µV/V"
chart2_name = "DUT DNL data, referenced to itself"
chart4_name = "Environment during points sweep"
chart3_name = "Difference between 34420A channels"
chart5_name = "Gain error relative to reference"
axis_y_label = axis_y_label + (", %s/V relative to 3x3458" % stats_units)

with open(fnout) as csvfile:
    print (fnout)
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    is_first = True
    for row in spamreader:
        if is_first:
            is_first = False
            continue
        #print ("%f" % float(row[1]))
        #ideal.extend([float(row[1]) ])
        #ideal.extend([ (float(row[2]) + float(row[3]) + float(row[4])) / 3 ])
        #ideal.extend([ (float(row[2]) + float(row[3])) / 2 ])
        #if ( (1e6 * float(row[10]) ) / ref_range1 ) < 0.04:
        if (1):
            idxr.extend([row[0]]) #3458
            cntr.extend([count])
            count = count + 1
            ideal.extend([ (float(row[2]) + float(row[3]) + float(row[4]) ) / 3 ])
            #ideal.extend([float(row[1])]) #3458
            #ideal2.extend([float(row[6])]) #3458
            real.extend([float(row[2])]) #3458
            real2.extend([float(row[3])]) # 3458
            real3.extend([float(row[4])]) # 3459
            real4.extend([float(row[5])]) # ch1
            real5.extend([float(row[6])]) # ch2
            real6.extend([float(row[7])]) # ch2
            real7.extend([float(row[8])]) # ch2
            real8.extend([float(row[9])]) # ch2
            real9.extend([float(row[10])]) # ch2
            knv = 3#float(row[7]) * 0.99599808
            #real6.extend([knv]) # 1801
            chdiff.extend([(float(row[5]) - float(row[6]) ) * 1e9 ])
            #gain1diff.extend([ (( float(row[5]) / float(row[1])) - 1) * 1e6 ])
            #gain2diff.extend([ (( float(row[6]) / float(row[1])) - 1) * 1e6 ])
            #gainhdiff.extend([ (( knv / float(row[6])) - 1) * 1e6 ])
            
            error1.extend([ (1e6 * float(row[11]) ) / ref_range1 ])
            error2.extend([ (1e6 * float(row[12]) ) / ref_range1 ])
            error3.extend([ (1e6 * float(row[13]) ) / ref_range1 ])
            error4.extend([ (1e6 * float(row[14]) ) / ref_range2 ])
            error5.extend([ (1e6 * float(row[15]) ) / ref_range2 ])
            error6.extend([ (1e6 * float(row[16]) ) / ref_range1 ])
            error7.extend([ (1e6 * float(row[17]) ) / ref_range1 ])
            error8.extend([ (1e6 * float(row[18]) ) / ref_range2 ])
            error9.extend([ (1e6 * float(row[19]) ) / ref_range2 ])
            
            ambient.extend([float(row[25])]) # 3458
            rh.extend([float(row[26])]) # 2002
            pressure.extend([float(row[27])]) # 5720
        else:
            continue
        
        #real5.extend([float(row[6])])
        #real6.extend([float(row[7])])

#print ("Reference data points: ")
print (np.max(error4))
print (np.max(error3))

p = np.polyfit(real,ideal,1)
pv = np.polyval(p,real)
diff = (ideal-pv)
diff_ppm = (diff/ref_range1)*1000000.0

p2 = np.polyfit(real2,ideal,1)
pv2 = np.polyval(p2,real2)
diff2 = (ideal-pv2)
diff_ppm2 = (diff2/ref_range1)*1000000.0

p3 = np.polyfit(real3,ideal,1)
pv3 = np.polyval(p3,real3)
diff3 = (ideal-pv3)
diff_ppm3 = (diff3/ref_range1)*1000000.0

p4 = np.polyfit(real4,ideal,1)
pv4 = np.polyval(p4,real4)
diff4 = (ideal-pv4)
diff_ppm4 = (diff4/ref_range2)*1000000.0
##
p5 = np.polyfit(real5,ideal,1)
pv5 = np.polyval(p5,real5)
diff5 = (ideal-pv5)
diff_ppm5 = (diff5/ref_range2)*1000000.0

p6 = np.polyfit(real6,ideal,1)
pv6 = np.polyval(p6,real6)
diff6 = (ideal-pv6)
diff_ppm6 = (diff6/ref_range1)*1000000.0

p7 = np.polyfit(real7,ideal,1)
pv7 = np.polyval(p7,real7)
diff7 = (ideal-pv7)
diff_ppm7 = (diff7/ref_range1)*1000000.0

p8 = np.polyfit(real8,ideal,1)
pv8 = np.polyval(p8,real8)
diff8 = (ideal-pv8)
diff_ppm8 = (diff8/ref_range2)*1000000.0

p9 = np.polyfit(real9,ideal,1)
pv9 = np.polyval(p9,real9)
diff9 = (ideal-pv9)
diff_ppm9 = (diff9/ref_range2)*1000000.0

# ref 3458

pb = np.polyfit(real,real,1)
pvb = np.polyval(pb,real)
diffb = real-pvb
diff_ppm1b = (diffb/ref_range1)*1000000.0

p2b = np.polyfit(real2,real2,1)
pv2b = np.polyval(p2b,real2)
diff2b = real2-pv2b
diff_ppm2b = (diff2b/ref_range1)*1000000.0

p3b = np.polyfit(real3,real3,1)
pv3b = np.polyval(p3b,real3)
diff3b = real3-pv3b
diff_ppm3b = (diff3b/ref_range1)*1000000.0

p4b = np.polyfit(real4,real4,1)
pv4b = np.polyval(p4b,real4)
diff4b = real4-pv4b
diff_ppm4b = (diff4b/ref_range2)*1000000.0
##
p5b = np.polyfit(real5,real5,1)
pv5b = np.polyval(p5b,real5)
diff5b = real5-pv5b
diff_ppm5b = (diff5b/ref_range2)*1000000.0

p6b = np.polyfit(real6,real6,1)
pv6b = np.polyval(p6b,real6)
diff6b = real6-pv6b
diff_ppm6b = (diff6b/ref_range1)*1000000.0

p7b = np.polyfit(real7,real7,1)
pv7b = np.polyval(p7b,real7)
diff7b = real7-pv7b
diff_ppm7b = (diff7b/ref_range1)*1000000.0

p8b = np.polyfit(real8,real8,1)
pv8b = np.polyval(p8b,real8)
diff8b = real8-pv8b
diff_ppm8b = (diff8b/ref_range2)*1000000.0

p9b = np.polyfit(real9,real9,1)
pv9b = np.polyval(p9b,real9)
diff9b = real9-pv9b
diff_ppm9b = (diff9b/ref_range2)*1000000.0

inl_max = np.amax(diff_ppm)
inl_min = np.amin(diff_ppm)
inl5b_max = np.amax(diff_ppm)
inl5b_min = np.amin(diff_ppm)

print (inl5b_max, inl5b_min)

err1_max = np.amax(error1)
err1_min = np.amin(error1)
err1_span = err1_max - err1_min

err5_max = np.amax(error2)
err5_min = np.amin(error2)
err5_span = err5_max - err5_min

amb_max = np.amax(ambient)
amb_min = np.amin(ambient)
amb_span = amb_max - amb_min

rh_max = np.amax(rh)
rh_min = np.amin(rh)
rh_span = rh_max - rh_min

inl_delta = inl_max - inl_min
inl_span = inl_delta / 2.0
inl5b_delta = inl5b_max - inl5b_min
inl5b_span = inl5b_delta / 2.0

### PLOTTING

fig, ((dx1, dx2), (dx3, dx4), (dx5, dx6), (dx7, dx8), (dx9, ax2), (ax4, hum)) = plt.subplots(6,2)
#plt.text(180, 0.6,'Rev 6, AUG.3.2024', horizontalalignment='left', verticalalignment='top', fontsize=9)
idx = 1

fig.suptitle(title_label, size=22)

dx1.patch.set_color('#ffffff')
fig.patch.set_facecolor('#eeeeff')
dx1.set_clip_on(False)

w = float(cfg.get('main', 'plot_w')) / 100
h = float(cfg.get('main', 'plot_h')) / 100
ws = float(cfg.get('main', 'plot_w_s')) / 100
hs = float(cfg.get('main', 'plot_h_s')) / 100
fig.set_size_inches(w,h)
plt.tight_layout(rect=[0.03, 0.03, 0.99, 0.98], w_pad=0.7, h_pad=0.2)                                # Reduce margins around the graph
plt.subplots_adjust(wspace=0.07,hspace=0.3)

#filtered1s = scipy.ndimage.filters.gaussian_filter1d(diff_ppm4,  sigma=3)
filtered1 = scipy.ndimage.gaussian_filter1d(diff_ppm,  sigma=1) #_ppm,  sigma=1)
filtered2 = scipy.ndimage.gaussian_filter1d(diff_ppm2, sigma=1) #_ppm2, sigma=1)
filtered3 = scipy.ndimage.gaussian_filter1d(diff_ppm3, sigma=1) #_ppm3, sigma=1)
filtered4 = scipy.ndimage.gaussian_filter1d(diff_ppm4, sigma=1) #_ppm4, sigma=1)
filtered5 = scipy.ndimage.gaussian_filter1d(diff_ppm5, sigma=1) #_ppm5, sigma=1)
filtered6 = scipy.ndimage.gaussian_filter1d(diff_ppm6, sigma=1) #_ppm6, sigma=1)
filtered7 = scipy.ndimage.gaussian_filter1d(diff_ppm7, sigma=1) #_ppm6, sigma=1)
filtered8 = scipy.ndimage.gaussian_filter1d(diff_ppm8, sigma=1) #_ppm6, sigma=1)
filtered9 = scipy.ndimage.gaussian_filter1d(diff_ppm9, sigma=1) #_ppm6, sigma=1)

filtered1b = scipy.ndimage.gaussian_filter1d(diff_ppm1b, sigma=1)
filtered2b = scipy.ndimage.gaussian_filter1d(diff_ppm2b, sigma=1)
filtered3b = scipy.ndimage.gaussian_filter1d(diff_ppm3b, sigma=1)
filtered4b = scipy.ndimage.gaussian_filter1d(diff_ppm4b, sigma=1)
filtered5b = scipy.ndimage.gaussian_filter1d(diff_ppm5b, sigma=1)
filtered6b = scipy.ndimage.gaussian_filter1d(diff_ppm6b, sigma=1)
filtered7b = scipy.ndimage.gaussian_filter1d(diff_ppm7b, sigma=1)
filtered8b = scipy.ndimage.gaussian_filter1d(diff_ppm8b, sigma=1)
filtered9b = scipy.ndimage.gaussian_filter1d(diff_ppm9b, sigma=1)

#for diff_ppm in diff_ppms:
#ax.plot(ideal, diff_ppm)
dataset_color1 =  '#540fff'
dataset_color2 =  '#0cbcff'
dataset_color3 =  '#800fff'
dataset_color4 =  '#ff0e41'
dataset_color5 =  '#ff9500'
dataset_color6 =  '#40916c'
dataset_color7 =  '#287272'
dataset_color8 =  '#c00000'
dataset_color9 =  '#800000'
dataset_color10 = '#333333'
dataset_color11 = '#ffcc22'
dataset_color12 = '#0000ff'

#ax4.plot(ideal, chdiff, dataset_color6, label='Data %i' % (1), alpha=0.7, linewidth=0.2, marker="p", markersize=8, markerfacecolor=dataset_color6)
#ax5.plot(ideal, gain1diff, dataset_color4, label='Data %i' % (1), alpha=0.7, linewidth=0.2, marker="p", markersize=8, markerfacecolor=dataset_color4)
#ax5.plot(ideal, gain2diff, dataset_color5, label='Data %i' % (1), alpha=0.7, linewidth=0.2, marker="p", markersize=8, markerfacecolor=dataset_color5)
#ax5.plot(ideal, gainhdiff, dataset_color3, label='Data %i' % (1), alpha=0.7, linewidth=0.2, marker="p", markersize=8, markerfacecolor=dataset_color3)

dx1.plot(ideal, filtered1, dataset_color1, label='Data %i' % (1), alpha=1, linewidth=4, marker="1", markersize=5, markerfacecolor=dataset_color1)
dx2.plot(ideal, filtered2, dataset_color2, label='Data %i' % (2), alpha=1, linewidth=4, marker="2", markersize=5, markerfacecolor=dataset_color2)
dx3.plot(ideal, filtered3, dataset_color3, label='Data %i' % (3), alpha=1, linewidth=4, marker="3", markersize=5, markerfacecolor=dataset_color3)
dx4.plot(ideal, filtered4, dataset_color4, label='Data %i' % (4), alpha=1, linewidth=4, marker="4", markersize=5, markerfacecolor=dataset_color4)
dx5.plot(ideal, filtered5, dataset_color5, label='Data %i' % (5), alpha=1, linewidth=4, marker="H", markersize=5, markerfacecolor=dataset_color12)
dx6.plot(ideal, filtered6, dataset_color6, label='Data %i' % (6), alpha=1, linewidth=4, marker="h", markersize=5, markerfacecolor=dataset_color6)
dx7.plot(ideal, filtered7, dataset_color7, label='Data %i' % (7), alpha=1, linewidth=4, marker="D", markersize=5, markerfacecolor=dataset_color6)
dx8.plot(ideal, filtered8, dataset_color8, label='Data %i' % (8), alpha=1, linewidth=4, marker="x", markersize=5, markerfacecolor=dataset_color6)
dx9.plot(ideal, filtered9, dataset_color9, label='Data %i' % (9), alpha=1, linewidth=4, marker="X", markersize=5, markerfacecolor=dataset_color6)
#ax.plot(ideal, filtered1s, "#000000", label='Data %i' % (1), alpha=0.8, linewidth=5, marker=",", markerfacecolor=dataset_color4)

ax2.plot(real,  filtered1b, dataset_color1, label='Data %i' % (1),  alpha=1, linewidth=1, marker="1", markerfacecolor=dataset_color1)
ax2.plot(real2, filtered2b, dataset_color2, label='Data %i' % (2), alpha=1, linewidth=1, marker="2", markerfacecolor=dataset_color2)
ax2.plot(real3, filtered3b, dataset_color3, label='Data %i' % (3), alpha=1, linewidth=1, marker="3", markerfacecolor=dataset_color3)
ax2.plot(real4, filtered4b, dataset_color4, label='Data %i' % (4), alpha=1, linewidth=1, marker="4", markerfacecolor=dataset_color4)
ax2.plot(real5, filtered5b, dataset_color5, label='Data %i' % (5), alpha=1, linewidth=1, marker="H", markerfacecolor=dataset_color5)
ax2.plot(real6, filtered6b, dataset_color6, label='Data %i' % (6), alpha=1, linewidth=1, marker="h", markerfacecolor=dataset_color6)
ax2.plot(real7, filtered7b, dataset_color7, label='Data %i' % (7), alpha=1, linewidth=1, marker="D", markerfacecolor=dataset_color7)
ax2.plot(real8, filtered8b, dataset_color8, label='Data %i' % (8), alpha=1, linewidth=1, marker="x", markerfacecolor=dataset_color8)
ax2.plot(real9, filtered9b, dataset_color9, label='Data %i' % (9), alpha=1, linewidth=1, marker="X", markerfacecolor=dataset_color9)

#ax2.errorbar(real4, filtered4b, yerr=error4, fmt=' ', alpha=0.9, linewidth=0.5, capsize=3, color=dataset_color4)
ax2.errorbar(real,  filtered1b, yerr=error1, fmt=' ', alpha=0.9, linewidth=1, capsize=3, color=dataset_color10)
ax2.errorbar(real2, filtered2b, yerr=error2, fmt=' ', alpha=0.9, linewidth=1, capsize=3, color=dataset_color10)
ax2.errorbar(real3, filtered3b, yerr=error3, fmt=' ', alpha=0.9, linewidth=1, capsize=3, color=dataset_color10)
ax2.errorbar(real4, filtered4b, yerr=error4, fmt=' ', alpha=0.9, linewidth=1, capsize=3, color=dataset_color10)
ax2.errorbar(real5, filtered5b, yerr=error5, fmt=' ', alpha=0.9, linewidth=1, capsize=3, color=dataset_color10)
ax2.errorbar(real6, filtered6b, yerr=error6, fmt=' ', alpha=0.9, linewidth=1, capsize=3, color=dataset_color10)
ax2.errorbar(real7, filtered7b, yerr=error7, fmt=' ', alpha=0.9, linewidth=1, capsize=3, color=dataset_color10)
ax2.errorbar(real8, filtered8b, yerr=error8, fmt=' ', alpha=0.9, linewidth=1, capsize=3, color=dataset_color10)
ax2.errorbar(real9, filtered9b, yerr=error9, fmt=' ', alpha=0.9, linewidth=1, capsize=3, color=dataset_color10)

dx1.errorbar(ideal, filtered1, yerr=error1, fmt=' ', alpha=0.5, linewidth=1, capsize=3, color=dataset_color10)
dx2.errorbar(ideal, filtered2, yerr=error2, fmt=' ', alpha=0.5, linewidth=1, capsize=3, color=dataset_color10)
dx3.errorbar(ideal, filtered3, yerr=error3, fmt=' ', alpha=0.5, linewidth=1, capsize=3, color=dataset_color10)
dx4.errorbar(ideal, filtered4, yerr=error4, fmt=' ', alpha=0.5, linewidth=1, capsize=3, color=dataset_color10)
dx5.errorbar(ideal, filtered5, yerr=error5, fmt=' ', alpha=0.5, linewidth=1, capsize=3, color=dataset_color10)
dx6.errorbar(ideal, filtered6, yerr=error6, fmt=' ', alpha=0.5, linewidth=1, capsize=3, color=dataset_color10)
dx7.errorbar(ideal, filtered7, yerr=error7, fmt=' ', alpha=0.5, linewidth=1, capsize=3, color=dataset_color10)
dx8.errorbar(ideal, filtered8, yerr=error8, fmt=' ', alpha=0.5, linewidth=1, capsize=3, color=dataset_color10)
dx9.errorbar(ideal, filtered9, yerr=error9, fmt=' ', alpha=0.5, linewidth=1, capsize=3, color=dataset_color10)

ax4.plot(ideal, ambient, "#332233", label='Data %i' % (4), alpha=0.8, linewidth=0, marker="^", markersize=8, markerfacecolor="#88aaaa")
hum.plot(ideal, rh, "#4322f3", label='Data %i' % (4), alpha=0.8, linewidth=0, marker="o", markersize=8, markerfacecolor="#88aaaa")

#ax3.axis([axis_x_min, axis_x_max, amb_min - 0.5, amb_max + 0.5])

#ax4.axis([axis_x_min, axis_x_max, 18, 28])
#ax5.axis([axis_x_min, axis_x_max, -1000, 1000])


dx1.set_xlim([axis_x_min, axis_x_max])
dx2.set_xlim([axis_x_min, axis_x_max])
dx3.set_xlim([axis_x_min, axis_x_max])
dx4.set_xlim([axis_x_min, axis_x_max])
dx5.set_xlim([axis_x_min, axis_x_max])
dx6.set_xlim([axis_x_min, axis_x_max])
dx7.set_xlim([axis_x_min, axis_x_max])
dx8.set_xlim([axis_x_min, axis_x_max])
dx9.set_xlim([axis_x_min, axis_x_max])
ax2.set_xlim([axis_x_min, axis_x_max])
ax4.set_xlim([axis_x_min, axis_x_max])
hum.set_xlim([axis_x_min, axis_x_max])

limref = 0.2

dx1.set_ylim([-limref, limref])
dx2.set_ylim([-limref, limref])
dx3.set_ylim([-limref, limref])
dx4.set_ylim([-limref, limref])
dx5.set_ylim([-limref, limref])
dx6.set_ylim([axis_y_min, axis_y_max])
dx7.set_ylim([axis_y_min, axis_y_max])
limdx8 = 10
dx8.set_ylim([-limdx8, limdx8])
limdx9 = 1
dx9.set_ylim([-limdx9, limdx9])
#ax2.set_xlim([axis_x_min, axis_x_max])
#ax4.set_xlim([axis_x_min, axis_x_max])
#hum.set_xlim([axis_x_min, axis_x_max])

#ax.axis([21, 25, axis_y_min, axis_y_max])
#ax2.axis([axis_x_min, axis_x_max, axis_y_min, axis_y_max])
#start2, end2 = ax2.get_ylim()
start2 = -0.3
end2 = 0.3
ax2.axis([axis_x_min, axis_x_max, start2, end2])
ax2.yaxis.set_ticks(np.arange(start2, end2, 0.06))
#ax2.axis([0, count, axis_y_min, axis_y_max])
#ax4.axis([0, count, np.amin(filtered1),np.amax(filtered1)])

# dataset_name2,  dataset_name3, dataset_name4,
# dataset_name2, dataset_name3, dataset_name4, 
dx1.legend ([dataset_name1, dataset_name10])
dx2.legend ([dataset_name2, dataset_name10])
dx3.legend ([dataset_name3, dataset_name10])
dx4.legend ([dataset_name4, dataset_name10])
dx5.legend ([dataset_name5, dataset_name10])
dx6.legend ([dataset_name6, dataset_name10])
dx7.legend ([dataset_name7, dataset_name10])
dx8.legend ([dataset_name8, dataset_name10])
dx9.legend ([dataset_name9, dataset_name10])

ax2.legend([dataset_name1, dataset_name2, dataset_name3, dataset_name4, dataset_name5, dataset_name6, dataset_name7, dataset_name8, dataset_name9])
ax4.legend(["Ambient temperature, °C"])
hum.legend(["Ambient humidity, %RH"])
#ax4.legend(['Interchannel difference (CH1 - CH2), nV'])
#ax5.legend(['Gain error, CH1 (LH1510 opto)', 'Gain error, CH2 (HSSR-8400 factory opto)', 'Gain error, HP3459X (vs 2x3458A REF)'])
#ax4.legend(["Ambient temperature, °C"])
#, dataset_name7, dataset_name8, dataset_name9, dataset_name10, dataset_name11, dataset_name12

#ax.text(0.2, 0.05, (" INL Max: %.3f %s/V, Min %.3f %s/V" % (inl5b_max ,stats_units , inl5b_min, stats_units)), horizontalalignment='left', verticalalignment='center', transform = ax.transAxes, bbox=dict(facecolor='white', alpha=0.65))
#ax.text(0.6, 0.05, (" INL span +/-%.3f %s/V" % (inl5b_span/2, stats_units)), horizontalalignment='left', verticalalignment='center', transform = ax.transAxes, bbox=dict(facecolor='white', alpha=0.65))

#ax2.text(0.1, 0.05, (" SDEV 2002KF Max: %.4f %s, Min %.4f %s" % (err5_max , stats_units,  err5_min, stats_units)), horizontalalignment='left', verticalalignment='center', transform = ax2.transAxes, bbox=dict(facecolor='white', alpha=0.65))
#ax2.text(0.6, 0.05, (" SDEV 2002KF span +/-%.4f %s, Median %.4f %s" % (err5_span/2, stats_units,  np.median(error5), stats_units)), horizontalalignment='left', verticalalignment='center', transform = ax2.transAxes, bbox=dict(facecolor='white', alpha=0.65))

if (amb_span < 0.25):
    temp_box_color = "#cff800"
elif (0.25 >= amb_span < 0.5):
    temp_box_color = "#ffbf65"
elif (0.5 >= amb_span < 1.0):
    temp_box_color = "#ffec59"
else:
    temp_box_color = "#ff5c77"
    
if (amb_span < 15):
    rh_box_color = "#00f8ee"
elif (15 >= amb_span < 60):
    rh_box_color = "#2fff25"
elif (60 >= amb_span):
    rh_box_color = "#ff5c00"

ax4.text(0.55, 0.05,(" Ambient T Max: %.2f °C, Min %.2f °C " % (amb_max , amb_min)), horizontalalignment='left', verticalalignment='center', transform = ax4.transAxes, bbox=dict(facecolor=temp_box_color, alpha=0.65))
ax4.text(0.8, 0.05, (" Ambient T span +/-%.2f °C peak" % (amb_span/2)), horizontalalignment='left', verticalalignment='center', transform = ax4.transAxes, bbox=dict(facecolor=temp_box_color, alpha=0.65))
hum.text(0.55, 0.05,(" Ambient H Max: %.2f %%RH, Min %.2f %%RH " % (rh_max , rh_min)), horizontalalignment='left', verticalalignment='center', transform = hum.transAxes, bbox=dict(facecolor=rh_box_color, alpha=0.65))
hum.text(0.8, 0.05, (" Ambient H span +/-%.2f %%RH peak" % (rh_span/2)), horizontalalignment='left', verticalalignment='center', transform = hum.transAxes, bbox=dict(facecolor=rh_box_color, alpha=0.65))

start, end = dx1.get_ylim()

#dx1.yaxis.set_ticks(np.arange(start, end, axis_y_step))
#ax.yaxis.set_ticks (np.arange(start, end, axis_y_step * 2))
#ax2.yaxis.set_ticks(np.arange(start2, end2, axis_y_step * 2))

startx, endx = dx1.get_xlim()

dx1.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))
dx2.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))
dx3.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))
dx4.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))
dx5.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))
dx6.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))
dx7.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))
dx8.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))
dx9.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))

dx1.yaxis.set_major_locator(ticker.MultipleLocator(0.03))
dx2.yaxis.set_major_locator(ticker.MultipleLocator(0.03))
dx3.yaxis.set_major_locator(ticker.MultipleLocator(0.03))
dx4.yaxis.set_major_locator(ticker.MultipleLocator(0.03))
dx5.yaxis.set_major_locator(ticker.MultipleLocator(0.03))
dx6.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
dx7.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
dx8.yaxis.set_major_locator(ticker.MultipleLocator(1))
dx9.yaxis.set_major_locator(ticker.MultipleLocator(0.1))

ax2.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))
#ax3.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))
ax4.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))
hum.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))
#ax5.xaxis.set_ticks(np.arange(startx, endx, axis_x_step))

dx1_title='%s REF, %s points, %.3f range' % (dataset_name1, count, ref_range1)
dx2_title='%s REF, %s points, %.3f range' % (dataset_name2, count, ref_range1)
dx3_title='%s REF, %s points, %.3f range' % (dataset_name3, count, ref_range1)
dx4_title='%s DMM, %s points, %.3f range' % (dataset_name4, count, ref_range2)
dx5_title='%s DMM, %s points, %.3f range' % (dataset_name5, count, ref_range2)
dx6_title='%s DMM, %s points, %.3f range' % (dataset_name6, count, ref_range1)
dx7_title='%s DMM, %s points, %.3f range' % (dataset_name7, count, ref_range1)
dx8_title='%s DUT, %s points, %.3f range' % (dataset_name8, count, ref_range2)
dx9_title='%s DUT, %s points, %.3f range' % (dataset_name9, count, ref_range2)

dx1.set (xlabel=axis_x_label, ylabel=axis_y_label)
dx2.set (xlabel=axis_x_label, ylabel=axis_y_label)
dx3.set (xlabel=axis_x_label, ylabel=axis_y_label)
dx4.set (xlabel=axis_x_label, ylabel=axis_y_label)
dx5.set (xlabel=axis_x_label, ylabel=axis_y_label)
dx6.set (xlabel=axis_x_label, ylabel=axis_y_label)
dx7.set (xlabel=axis_x_label, ylabel=axis_y_label)
dx8.set (xlabel=axis_x_label, ylabel=axis_y_label)
dx9.set (xlabel=axis_x_label, ylabel=axis_y_label)

dx1.set_title(dx1_title, color='blue')
dx2.set_title(dx2_title, color='blue')
dx3.set_title(dx3_title, color='blue')
dx4.set_title(dx4_title, color='black')
dx5.set_title(dx5_title, color='black')
dx6.set_title(dx6_title, color='black')
dx7.set_title(dx7_title, color='black')
dx8.set_title(dx8_title, color='red')
dx9.set_title(dx9_title, color='brown')

ax2.set(xlabel=axis2_x_label, ylabel=axis2_y_label,  title='%s' % (chart2_name))
#ax3.set(xlabel=axis_x_label, ylabel=axis3_y_label, title='%s' % (chart3_name))
ax4.set(xlabel=axis_x_label, ylabel=axis4_y_label, title='%s' % (chart4_name))
hum.set(xlabel=axis_x_label, ylabel=axis5_y_label, title='%s' % (chart5_name))

#ax3.yaxis.set_ticks(np.arange(start3, end3, axis_y_step))
#start3, end3 = ax3.get_ylim()

#ax2.xaxis.set_ticks(np.arange(0, count, 2))

#start4, end4 = ax4.get_ylim()
#ax4.yaxis.set_ticks(np.arange(start4, end4, axis_y_step))
#ax4.xaxis.set_ticks(np.arange(0, count, 20))

dx1.grid ()
dx2.grid ()
dx3.grid ()
dx4.grid ()
dx5.grid ()
dx6.grid ()
dx7.grid ()
dx8.grid ()
dx9.grid ()

ax2.grid()
#ax3.grid()
ax4.grid()
#ax5.grid()

dx1.text(0.1, 0.05,'xDevs.com | https://github.com/tin-/linkit',horizontalalignment='center',verticalalignment='center',transform = dx1.transAxes)
dx2.text(0.1, 0.05,'xDevs.com | https://github.com/tin-/linkit',horizontalalignment='center',verticalalignment='center',transform = dx2.transAxes)
dx3.text(0.1, 0.05,'xDevs.com | https://github.com/tin-/linkit',horizontalalignment='center',verticalalignment='center',transform = dx3.transAxes)
dx4.text(0.1, 0.05,'xDevs.com | https://github.com/tin-/linkit',horizontalalignment='center',verticalalignment='center',transform = dx4.transAxes)
dx5.text(0.1, 0.05,'xDevs.com | https://github.com/tin-/linkit',horizontalalignment='center',verticalalignment='center',transform = dx5.transAxes)
dx6.text(0.1, 0.05,'xDevs.com | https://github.com/tin-/linkit',horizontalalignment='center',verticalalignment='center',transform = dx6.transAxes)
dx7.text(0.1, 0.05,'xDevs.com | https://github.com/tin-/linkit',horizontalalignment='center',verticalalignment='center',transform = dx7.transAxes)
dx8.text(0.1, 0.05,'xDevs.com | https://github.com/tin-/linkit',horizontalalignment='center',verticalalignment='center',transform = dx8.transAxes)
dx9.text(0.1, 0.05,'xDevs.com | https://github.com/tin-/linkit',horizontalalignment='center',verticalalignment='center',transform = dx9.transAxes)

png_fn_large = fn.split("GPIB5.dsv")[0] + ".png"
png_fn_small = fn.split("GPIB5.dsv")[0] + "_1.png"

ax2.text(0.1, -0.15,'xDevs.com | https://github.com/tin-/linkit',horizontalalignment='center',verticalalignment='center',transform = ax2.transAxes)

fig.savefig(png_fn_large, facecolor=fig.get_facecolor(), transparent=False)
#ax3.yaxis.set_ticks (np.arange(start3, end3, axis_y_step * 2))
plt.tight_layout(rect=[0.03, 0.035, 1.0, 0.98], w_pad=0.5, h_pad=2.5)                                # Reduce margins around the graph
plt.subplots_adjust(wspace=0.07,hspace=0.3)
figs = fig
figs.set_size_inches(ws,hs)
figs.savefig(png_fn_small, facecolor=figs.get_facecolor(), transparent=False)
plt.show()