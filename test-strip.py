#!/usr/bin/env python3

import os
import sys
import argparse
import asyncio

from rpi_ws281x import Color

from LEDStrip import LEDStrip

# Main program logic follows:
if __name__ == '__main__':
    # must be run as root
    if not os.geteuid() == 0:
        sys.exit('This script must be run as root in order to control the LED.')

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_leds', type=int, help='number of LEDs in the strip', default=1)
    args = parser.parse_args()

    strip = LEDStrip(args.num_leds)

    try:
        while True:
            print('Color wipe animations.')
            await strip.colorWipe(Color(255, 0, 0))  # Red wipe
            await strip.colorWipe(Color(0, 255, 0))  # Blue wipe
            await strip.colorWipe(Color(0, 0, 255))  # Green wipe
            print('Theater chase animations.')
            await strip.theaterChase(Color(127, 127, 127))  # White theater chase
            await strip.theaterChase(Color(127, 0, 0))  # Red theater chase
            await strip.theaterChase(Color(0, 0, 127))  # Blue theater chase
            print('Rainbow animations.')
            await strip.rainbow()
            await strip.rainbowCycle()
            await strip.theaterChaseRainbow()

    except KeyboardInterrupt:
        await strip.colorWipe(Color(0, 0, 0), 10)
