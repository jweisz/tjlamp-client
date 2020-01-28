import asyncio
from rpi_ws281x import PixelStrip, Color
from matplotlib import colors

class LEDStrip():
    def __init__(self, count, pin=18, freq_hz=800000, dma=10, invert=False, brightness=255, channel=0):
        print(f"💡 initializing LED strip with {count} neopixels")

        # Create NeoPixel object with appropriate configuration.
        self.strip = PixelStrip(count, pin, freq_hz, dma, invert, brightness, channel)

        # Intialize the library (must be called once before other functions).
        self.strip.begin()

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
        print(f"🐞 colorFromName: {name}")
        rgba = colors.to_rgba(name)
        r = int(255*rgba[0])
        g = int(255*rgba[1])
        b = int(255*rgba[2])
        print(f"🐞 colorFromName r: {r}, g: {g}, b: {b}")
        return Color(r, g, b)

    # Get a Color from its hex value
    def colorFromHex(self, hex):
        print(f"🐞 colorFromHex: {hex}")
        rgb = (0,0,0)
        if hex.startswith('#'):
            rgb = colors.hex2color(hex)
        else:
            rgb = colors.hex2color('#' + hex)
        r = int(255*rgb[0])
        g = int(255*rgb[1])
        b = int(255*rgb[2])
        print(f"🐞 colorFromHex r: {r}, g: {g}, b: {b}")
        return Color(r, g, b)
    
    # Get a Color from it's name or hex value
    def parseColor(self, color):
        print(f"🐞 parseColor: {color}")
        c = Color(255, 255, 255)
        if color.startswith('#'):
            print(f"🐞 parseColor it's hex!")
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
            await asyncio.sleep(wait_ms / 1000.0)

    async def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                await asyncio.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    async def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            await asyncio.sleep(wait_ms / 1000.0)

    async def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel(
                    (int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            await asyncio.sleep(wait_ms / 1000.0)

    async def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()
                await asyncio.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)
