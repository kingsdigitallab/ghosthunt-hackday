import unicornhat as unicorn
import os
import datetime
import time

#unicorn hat light test

# Init Unicorn
unicorn.set_layout(unicorn.AUTO)
# hold portrat style with usbs at bottom
unicorn.rotation(270)
unicorn.brightness(0.2)
width,height=unicorn.get_shape()
# minimum db signal
min = 46

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
    for db in range(min, 0, -1):
        unicorn.clear()
        _display_unicorn(float(db*-1))
        unicorn.show()
        time.sleep(0.5)