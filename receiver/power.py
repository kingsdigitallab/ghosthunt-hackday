from rtlsdr import *
from pylab import *
import time
import math
import unicornhat as unicorn
import os
import datetime

# Radio test script for Ghost Hunt Hackday
# Written by Brian Maher 31/1/2018
# Modified by Elliott Hall

# Init Unicorn
unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.2)
width,height=unicorn.get_shape()

sdr = RtlSdr()
sdr.sample_rate = 3.2e6
sdr.center_freq = 885e5
sdr.gain = 20

if not os.path.exists('power.log'):
    with open('power.log', 'wt') as f:
        f.write("Power Script Log\n\n")

def _get_pixel_count(db):
    # crude
    count = 64
    db = int(db)
    count = count + db
    return count

def _display_unicorn(db):
    # turn db into % and display in unicorn
    min = 46
    percent = (1 - ((db*-1) / min)) * 100
    # Over 50 add red line

while True:
    samples = sdr.read_samples(500e3)
    db = 10*log10(var(samples))
    print 'relative power: %0.1f dB' % (10*log10(var(samples)))
    with open('power.log', 'ab') as f:
        f.write("[{}] {} dB\n".format(datetime.datetime.now(),  (10*log10(var(samples)))))
    num_pixels = _get_pixel_count(db)
    cur_pixel = 0
    for x in range(height):
        for y in range(width):
            if cur_pixel < num_pixels:
                unicorn.set_pixel(x,y,0,255,0)
            else:
                unicorn.set_pixel(x,y,0,0,0) 
            cur_pixel = cur_pixel + 1
            unicorn.show()
