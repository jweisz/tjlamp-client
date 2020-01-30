#!/usr/bin/env python3

import os
import sys
import time
import json
import argparse
import asyncio
import websockets
import configparser

from LEDStrip import LEDStrip

async def listen(uri, num_leds):
    strip = LEDStrip(num_leds)
    strip.blankStrip()

    async with websockets.connect(uri) as websocket:
        print(f"🔌 connected to {uri}…")
        await strip.quickFlash(strip.colorFromHex("#445500"), 3)

        async for message in websocket:
            # message = await websocket.recv()
            print(f"🎉 received message: {message}")
            msg = json.loads(message)
            cmd = msg.get('cmd', '')
            
            # shine -> stripColor(color)
            # pulse -> theaterChase(color)
            # rainbow -> rainbowCycle()
            # rainbowPulse -> theaterChaseRainbow()
            # off -> blankStrip()
            if cmd == 'shine':
                color = msg.get('color', '#FFFFFF')

                if color == 'rainbow':
                    print(f"❤️💙💚💜💛🧡🤍 rainbow!")
                    strip.rainbowCycle()
                else:
                    c = strip.parseColor(color)
                    print(f"💡 shining with color {color}: {strip.colorToHex(c)}")
                    strip.stripColor(c)
            
            elif cmd == 'pulse':
                color = msg.get('color', '#FFFFFF')

                if color == 'rainbow':
                    print(f"❤️💙💚💜💛🧡🤍 pulsing rainbow!")
                    strip.theaterChaseRainbow()
                else:
                    c = strip.parseColor(color)
                    print(f"💡 pulsing with color {color}: {strip.colorToHex(c)}")
                    strip.theaterChase(c)
            
            elif cmd == 'on':
                print(f"💡 lights on")
                c = strip.parseColor('#FFFFFF')
                strip.stripColor(c)
            
            elif cmd == 'off':
                print(f"💡 lights out")
                strip.blankStrip()
    
    print(f"🔌 disconnected, panic!")
    for _ in range(3):
        await strip.panic()
        await asyncio.sleep(2)


# Main program logic follows:
if __name__ == '__main__':
    # must be run as root
    if not os.geteuid() == 0:
        sys.exit('This script must be run as root in order to control the LED.')

    # figure out where the config file is
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, help='path to config.ini file', default='')
    args = parser.parse_args()

    # load config params
    ws_url = 'ws://localhost:8080/lamp'
    num_leds = 60
    if args.config != '' and os.path.exists(args.config):
        config = configparser.ConfigParser()
        config.read(args.config)
        ws_url = config['tjlamp'].get('ws_url')
        num_leds = config['tjlamp'].get('num_leds')
        num_leds = int(num_leds)

    # open the web socket and listen for commands
    asyncio.get_event_loop().run_until_complete(listen(ws_url, num_leds))
