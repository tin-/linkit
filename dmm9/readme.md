# Combined linearity test for nine DMM, using DC Voltage source

DMM9 experiment
------------

This directory contains the data collected on 9 different DMMs with DC voltage performance sample. Process very similar to what's explained in [this xDevs.com article](https://xdevs.com/article/inlperf/).

Source was connected in parallel to all DMMs. Python script was used to perform programming of the instruments and setting random voltage point to 6 digits of resolution.
In this experiment [rebuilt Fluke 5720A calibrator was utilized](https://xdevs.com/article/hulk)

Multimeters were used in locked range at 12 V or 21 V (or 20 V for Datron 1281).

* [Hewlett-Packard 3458A 8&frac12;-digit DMM](https://xdevs.com/fix/hp3458) - with lowered temperature for LTZ oven A9 and golden A3.
* [Hewlett-Packard 3458A 8&frac12;-digit DMM](https://xdevs.com/fix/hp3458_u2) - with [twin xDevs.com X9D Analog ADR1000 reference](https://xdevs.com/pow/x9d_mod/)
* [Hewlett-Packard 3458A 8&frac12;-digit DMM](https://xdevs.com/pow/hp3458ff)
* [Keithley 2002 8&frac12;-digit DMM](https://xdevs.com/fix/kei2002_u2) with [modified binding posts](https://xdevs.com/article/kei2002ltc/)
* [Datron 1281 8&frac12;-digit DMM](https://xdevs.com/fix/d1281)
* [Hewlett-Packard 34420A 7&frac12;-digit DVM/nanovoltmeter](https://xdevs.com/fix/hp34420a_u2/)
* [Hewlett-Packard 34401A 6&frac12;-digit DMM](https://xdevs.com/pow/hp34401a_pow/)
* Broken Keithley 2002 7&frac12;-digit DMM
* Keithley 2002M 7&frac12;-digit DMM freshly adjusted

Data in this repository was collected and analyzed for an example how INL in sub-ppm level can be measured using conventional metrology equipment.

