#!/usr/bin/env python3

import os
import sys
import time
import json
import argparse
import asyncio
import websockets
from rpi_ws281x import PixelStrip, Color

class LEDStrip():
    def __init__(self, count, pin=18, freq_hz=80000, dma=10, invert=False, brightness=255, channel=0):
        # Create NeoPixel object with appropriate configuration.
        self.strip = PixelStrip(count, pin, freq_hz, dma, invert, brightness, channel)

        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    # Set the strip to a single color
    async def stripColor(self, color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    # Define functions which animate LEDs in various ways.
    async def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    async def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    async def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    async def rainbow(wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    async def rainbowCycle(wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, wheel(
                    (int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    async def theaterChaseRainbow(wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, wheel((i + j) % 255))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

async def listen():
    strip = LEDStrip(1)
    uri = "ws://tjlamp.mybluemix.net:80/lamp"
    async with websockets.connect(uri) as websocket:
        message = await websocket.recv()
        print(f"received message: {message}")
        msg = json.loads(message)
        cmd = msg.get('cmd', '')
        
        if cmd == 'shine':
            color = msg.get('color', '#FFFFFF')
            print(f" > shining with color {color}")
            await asyncio.create_task(strip.stripColor(color))
            
        elif cmd == 'rainbow':
            await asyncio.create_task(strip.rainbow())

        elif cmd == 'off':
            await asyncio.create_task(strip.stripColor('#000000'))

# Main program logic follows:
if __name__ == '__main__':
    # must be run as root
    if not os.geteuid() == 0:
        sys.exit('This script must be run as root in order to control the LED.')

    # open the web socket and listen for commands
    asyncio.get_event_loop().run_until_complete(listen())
