import asyncio
import random
from rpi_ws281x import PixelStrip, Color
from matplotlib import colors

class LEDStrip():
    def __init__(self, count, pin=18, freq_hz=800000, dma=10, invert=False, brightness=255, channel=0):
        print(f"💡 initializing LED strip with {count} neopixels on pin {pin}")

        # Create NeoPixel object with appropriate configuration.
        self.strip = PixelStrip(count, pin, freq_hz, dma, invert, brightness, channel)

        # Intialize the library (must be called once before other functions).
        self.strip.begin()

        # Keep an asyncio task around so we can drive the LED asynchronously
        self.task = None

    # Generate colors around the color wheel
    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)
    
    # Get a Color from its name
    def colorFromName(self, name):
        rgba = colors.to_rgba(name)
        r = int(255*rgba[0])
        g = int(255*rgba[1])
        b = int(255*rgba[2])
        return Color(r, g, b)

    # Get a Color from its hex value
    def colorFromHex(self, hex):
        rgb = (0,0,0)
        if hex.startswith('#'):
            rgb = colors.hex2color(hex)
        else:
            rgb = colors.hex2color('#' + hex)
        r = int(255*rgb[0])
        g = int(255*rgb[1])
        b = int(255*rgb[2])
        return Color(r, g, b)
    
    # Get a Color from it's name or hex value
    def parseColor(self, color):
        c = Color(255, 255, 255)
        if color.startswith('#'):
            c = self.colorFromHex(color)
        else:
            try:
                c = self.colorFromName(color)
            except ValueError:
                try:
                    c = self.colorFromHex(color)
                except ValueError:
                    pass
        return c
    
    # Convert a Color to hex
    def colorToHex(self, color):
        return hex(color)
    
    # Covert HSV to RGB
    def hsvToRgb(self, h, s, v):
        if s == 0.0: return (v, v, v)
        i = int(h*6.)
        f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)
    
    # Run a new task in the background, cancelling any previous running task
    def runTask(self, func):
        async def _runTask(func):
            # cancel any existing task
            await self.cancelTask()

            # blank the LEDs
            await self._blankStrip()
    
            # fire up the new task
            self.task = asyncio.create_task(func)
        asyncio.create_task(_runTask(func))
    
    # Cancel the currently running task
    async def cancelTask(self):
        if not self.task is None:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass

    # Functions which illuminate / animate LEDs in various ways.
    # These are all defined synchronously, and they work by running an asynchronous
    # task in the background (so we can drive the LEDs while also listening on the 
    # websocket for new commands)
    def stripColor(self, color):
        """Shine the LEDs the given color"""
        async def _stripColor(color):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
            self.strip.show()
        self.runTask(_stripColor(color))
    
    def blankStrip(self):
        """Turn off all the LEDs (as a background task)"""
        self.runTask(self._blankStrip())
    
    async def _blankStrip(self):
        """Turn off all the LEDs (as a foreground task)"""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, 0)
        self.strip.show()
        
    def colorWipe(self, color, wait_ms=50):
        """Wipe a color across display a pixel at a time."""
        async def _colorWipe(color, wait_ms):
            try:
                while True:
                    for i in range(self.strip.numPixels()):
                        self.strip.setPixelColor(i, color)
                        self.strip.show()
                        await asyncio.sleep(wait_ms / 1000.0)
            except asyncio.CancelledError:
                await self._blankStrip()
        self.runTask(_colorWipe(color, wait_ms))

    def theaterChase(self, color, wait_ms=50):
        """Movie theater light style chaser animation."""
        async def _theaterChase(color, wait_ms):
            try:
                while True:
                    for q in range(3):
                        for i in range(0, self.strip.numPixels(), 3):
                            self.strip.setPixelColor(i + q, color)
                        self.strip.show()
                        await asyncio.sleep(wait_ms / 1000.0)
                        for i in range(0, self.strip.numPixels(), 3):
                            self.strip.setPixelColor(i + q, 0)
            except asyncio.CancelledError:
                await self._blankStrip()
        self.runTask(_theaterChase(color, wait_ms))

    def rainbow(self, wait_ms=20):
        """Draw rainbow that fades across all pixels at once."""
        async def _rainbow(wait_ms, iterations):
            try:
                while True:
                    for j in range(256 * iterations):
                        for i in range(self.strip.numPixels()):
                            self.strip.setPixelColor(i, self.wheel((i + j) & 255))
                        self.strip.show()
                        await asyncio.sleep(wait_ms / 1000.0)
            except asyncio.CancelledError:
                await self._blankStrip()
        self.runTask(_rainbow(wait_ms, 1))

    def rainbowCycle(self, wait_ms=20):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        async def _rainbowCycle(wait_ms, iterations):
            try:
                while True:
                    for j in range(256 * iterations):
                        for i in range(self.strip.numPixels()):
                            self.strip.setPixelColor(i, self.wheel(
                                (int(i * 256 / self.strip.numPixels()) + j) & 255))
                        self.strip.show()
                        await asyncio.sleep(wait_ms / 1000.0)
            except asyncio.CancelledError:
                await self._blankStrip()
        self.runTask(_rainbowCycle(wait_ms, 5))

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        async def _theaterChaseRainbow(wait_ms):
            try:
                while True:
                    for j in range(256):
                        for q in range(3):
                            for i in range(0, self.strip.numPixels(), 3):
                                self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                            self.strip.show()
                            await asyncio.sleep(wait_ms / 1000.0)
                            for i in range(0, self.strip.numPixels(), 3):
                                self.strip.setPixelColor(i + q, 0)
            except asyncio.CancelledError:
                await self._blankStrip()
        self.runTask(_theaterChaseRainbow(wait_ms))
    
    async def panic(self):
        """Three fast pulses of red."""
        await self.quickFlash(Color(255, 0, 0), 3)
    
    async def quickFlash(self, color, n_pulses=3, wait_ms=50):
        def on():
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
            self.strip.show()
        def off():
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 0, 0))
            self.strip.show()
        for i in range(n_pulses):
            on()
            await asyncio.sleep(wait_ms / 1000.0)
            off()
            await asyncio.sleep(wait_ms / 1000.0)

    def disco(self, servo):
        """Pick a random color, hopefully far away enough from the previous color"""
        def _randomColor(h):
            next_h = (h + random.random() + 0.05) % 1.0
            s = 0.8 + (random.random() % 0.2)
            v = 0.8 + (random.random() % 0.2)
            return (next_h, s, v)
        
        """Disco mode!"""
        async def _disco(servo):
            try:
                h = random.random()

                while True:
                    # random color
                    (h, s, v) = _randomColor(h)
                    (r, g, b) = self.hsvToRgb(h, s, v)
                    self.theaterChase(Color(int(r*255), int(g*255), int(b*255)))

                    # random wave count, [1-2] times
                    await servo.wave(random.randint(1, 2))

                    # random sleep, [1-5] seconds
                    duration = random.randint(1, 5)
                    await asyncio.sleep(duration)
            except asyncio.CancelledError:
                await self._blankStrip()
        self.runTask(_disco(servo))
