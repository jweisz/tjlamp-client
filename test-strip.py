#!/usr/bin/env python3

import os
import sys
import argparse
import asyncio

from rpi_ws281x import Color

from LEDStrip import LEDStrip

async def main(args):
    strip = LEDStrip(args.num_leds)
    sleep_time = 5

    try:
        while True:
            print('Color wipe animations.')
            strip.colorWipe(Color(255, 0, 0))  # Red wipe
            await asyncio.sleep(sleep_time)
            strip.colorWipe(Color(0, 255, 0))  # Blue wipe
            await asyncio.sleep(sleep_time)
            strip.colorWipe(Color(0, 0, 255))  # Green wipe
            await asyncio.sleep(sleep_time)
            print('Theater chase animations.')
            strip.theaterChase(Color(127, 127, 127))  # White theater chase
            await asyncio.sleep(sleep_time)
            strip.theaterChase(Color(127, 0, 0))  # Red theater chase
            await asyncio.sleep(sleep_time)
            strip.theaterChase(Color(0, 0, 127))  # Blue theater chase
            await asyncio.sleep(sleep_time)
            print('Rainbow animations.')
            strip.rainbow()
            await asyncio.sleep(sleep_time)
            strip.rainbowCycle()
            await asyncio.sleep(sleep_time)
            strip.theaterChaseRainbow()
            await asyncio.sleep(sleep_time)

    except KeyboardInterrupt:
        strip.colorWipe(Color(0, 0, 0), 10)

# Main program logic follows:
if __name__ == '__main__':
    # must be run as root
    if not os.geteuid() == 0:
        sys.exit('This script must be run as root in order to control the LED.')

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_leds', type=int, help='number of LEDs in the strip', default=60)
    args = parser.parse_args()

    asyncio.get_event_loop().run_until_complete(main(args))
