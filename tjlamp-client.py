#!/usr/bin/env python3

import os
import sys
import time
import json
import argparse
import asyncio
import websockets

from LEDStrip import LEDStrip

async def listen():
    strip = LEDStrip(1)
    uri = "ws://tjlamp.mybluemix.net:80/lamp"
    async with websockets.connect(uri) as websocket:
        print(f"🔌 connected to {uri}…")
        async for message in websocket:
            message = await websocket.recv()
            print(f"🎉 received message: {message}")
            msg = json.loads(message)
            cmd = msg.get('cmd', '')
            
            if cmd == 'shine':
                color = msg.get('color', '#FFFFFF')
                c = strip.parseColor(color)
                print(f"💡 shining with color {color}: {c}")
                await asyncio.create_task(strip.stripColor(c))
                
            elif cmd == 'rainbow':
                print(f"❤️💙💚💜💛🧡🤍 rainbow!")
                await asyncio.create_task(strip.rainbow())

            elif cmd == 'off':
                print(f"💡 lights out")
                c = strip.parseColor('black')
                await asyncio.create_task(strip.stripColor(c))
    print(f"🔌 disconnected")

# Main program logic follows:
if __name__ == '__main__':
    # must be run as root
    if not os.geteuid() == 0:
        sys.exit('This script must be run as root in order to control the LED.')

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_leds', type=int, help='number of LEDs in the strip', default=1)
    args = parser.parse_args()

    # open the web socket and listen for commands
    n = args.num_leds
    asyncio.get_event_loop().run_until_complete(listen(n))
