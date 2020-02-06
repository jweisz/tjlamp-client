#!/usr/bin/env python3

import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
import wiringpi
import asyncio

async def main():
    GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the BCM layout

    # Set up pin 13 for PWM
    GPIO.setup(13, GPIO.OUT)  # Sets up pin 13 to an output (instead of an input)
    p = GPIO.PWM(13, 50)      # Sets up pin 13 as a PWM pin
    p.start(0)                # Starts running PWM on the pin and sets it to 0

    # Move the servo back and forth
    p.ChangeDutyCycle(3)     # Changes the pulse width to 3 (so moves the servo)
    await asyncio.sleep(1)                 # Wait 1 second
    p.ChangeDutyCycle(12)    # Changes the pulse width to 12 (so moves the servo)
    await asyncio.sleep(1)

    # Clean up everything
    p.stop()                 # At the end of the program, stop the PWM
    GPIO.cleanup()           # Resets the GPIO pins back to defaults

async def main2():
    # use 'GPIO naming'
    wiringpi.wiringPiSetupGpio()
    
    # set #13 to be a PWM output
    wiringpi.pinMode(13, wiringpi.GPIO.PWM_OUTPUT)
    
    # set the PWM mode to milliseconds stype
    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
    
    # divide down clock
    wiringpi.pwmSetClock(192)
    wiringpi.pwmSetRange(2000)
    
    while True:
        for pulse in range(50, 250, 10):
                wiringpi.pwmWrite(13, pulse)
                await asyncio.sleep(1)
        for pulse in range(250, 50, -10):
                wiringpi.pwmWrite(13, pulse)
                await asyncio.sleep(1)

# TJBot.prototype._SERVO_ARM_BACK = 500;
# TJBot.prototype._SERVO_ARM_UP = 1400;
# TJBot.prototype._SERVO_ARM_DOWN = 2300;

    # try:
    #     while True:
    #         print('Color wipe animations.')
    #         await strip.colorWipe(Color(255, 0, 0))  # Red wipe
    #         await strip.colorWipe(Color(0, 255, 0))  # Blue wipe
    #         await strip.colorWipe(Color(0, 0, 255))  # Green wipe
    #         print('Theater chase animations.')
    #         await strip.theaterChase(Color(127, 127, 127))  # White theater chase
    #         await strip.theaterChase(Color(127, 0, 0))  # Red theater chase
    #         await strip.theaterChase(Color(0, 0, 127))  # Blue theater chase
    #         print('Rainbow animations.')
    #         await strip.rainbow()
    #         await strip.rainbowCycle()
    #         await strip.theaterChaseRainbow()

    # except KeyboardInterrupt:
    #     await strip.colorWipe(Color(0, 0, 0), 10)

# Main program logic follows:
if __name__ == '__main__':
    # must be run as root
    #if not os.geteuid() == 0:
    #    sys.exit('This script must be run as root in order to control the servo.')

    #parser = argparse.ArgumentParser()
    #parser.add_argument('-n', '--num_leds', type=int, help='number of LEDs in the strip', default=1)
    #args = parser.parse_args()

    asyncio.get_event_loop().run_until_complete(main2())
