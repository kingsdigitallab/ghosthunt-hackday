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
unicorn.rotation(270)
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
    print(db)
    percent = round((1 - ((db*-1) / min)) * 100)
    print(percent)
    white = percent
    if percent > 50:
        red = 255
        white = percent - 50
    else:
        red=0
    # set red column
    for x in range(height):
        unicorn.set_pixel(0, x, red, 0, 0)

    cur_pixel = 0
    for y in range(height):
        for x in range(1, width):
            if cur_pixel < white:
                unicorn.set_pixel(x, y, 255, 255, 255)
            else:
                break
            cur_pixel = cur_pixel + 1



while True:
    unicorn.clear()
    samples = sdr.read_samples(500e3)
    db = 10*log10(var(samples))
    print 'relative power: %0.1f dB' % (10*log10(var(samples)))
    with open('power.log', 'ab') as f:
        f.write("[{}] {} dB\n".format(datetime.datetime.now(),  (10*log10(var(samples)))))
    _display_unicorn(float(db))
    unicorn.show()
