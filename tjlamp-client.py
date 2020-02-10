#!/usr/bin/env python3

import os
import sys
import time
import json
import asyncio
import argparse
import websockets
import configparser

from LEDStrip import LEDStrip
from Servo import ServoPigpio

async def listen(config):
    ws_url = config['tjlamp'].get('ws_url')
    num_leds = int(config['tjlamp'].get('num_leds'))
    led_pin = int(config['tjlamp'].get('led_pin'))
    led_brightness = config['tjlamp'].get('led_brightness')
    led_brightness = max(0, min(int(led_brightness), 255))
    servo_pin = int(config['tjlamp'].get('servo_pin'))
    enable_wave = config['tjlamp'].get('enable_wave').lower() in ("yes", "true", "t", "1")

    strip = LEDStrip(num_leds, pin=led_pin, brightness=led_brightness)
    strip.blankStrip()

    arm = ServoPigpio(servo_pin, enable_wave)

    print(f"🔌 connecting to {ws_url}…")
    async with websockets.connect(ws_url) as websocket:
        print(f"🔌 connected to {ws_url}…")
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
            # wave -> wave()
            # disco -> disco()
            if cmd == 'shine':
                color = msg.get('color', '#FFFFFF')

                if color == 'rainbow':
                    print(f"❤️💙💚💜💛🧡🤍 rainbow!")
                    strip.rainbowCycle()
                    arm.wave(2)
                elif color == 'disco':
                    print(f"🎊 disco mode!")
                    strip.disco(arm)
                else:
                    c = strip.parseColor(color)
                    print(f"💡 shining with color {color}: {strip.colorToHex(c)}")
                    strip.stripColor(c)

                    if not color == 'black':
                        arm.wave(2)
            
            elif cmd == 'pulse':
                color = msg.get('color', '#FFFFFF')

                if color == 'rainbow':
                    print(f"❤️💙💚💜💛🧡🤍 pulsing rainbow!")
                    strip.theaterChaseRainbow()
                    arm.wave(2)
                else:
                    c = strip.parseColor(color)
                    print(f"💡 pulsing with color {color}: {strip.colorToHex(c)}")
                    strip.theaterChase(c)
                    arm.wave(2)
            
            elif cmd == 'on':
                print(f"💡 lights on")
                c = strip.parseColor('#FFFFFF')
                strip.stripColor(c)
                arm.wave(2)
            
            elif cmd == 'off':
                print(f"💡 lights out")
                strip.blankStrip()
            
            elif cmd == 'wave':
                print(f"💪 waving")
                arm.wave(1)
    
    print(f"🔌 disconnected, panic!")
    for _ in range(3):
        arm.wave(1)
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
        print(f"🛠 reading config from {args.config}")
        config = configparser.ConfigParser()
        config.read(args.config)

    # open the web socket and listen for commands
    asyncio.get_event_loop().run_until_complete(listen(config))
