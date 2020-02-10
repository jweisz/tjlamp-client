#!/usr/bin/env python3

import argparse
import wiringpi
import asyncio

from Servo import Servo

def armBack(pin):
    wiringpi.pwmWrite(pin, 60)

def armUp(pin):
    wiringpi.pwmWrite(pin, 140)

def armDown(pin):
    wiringpi.pwmWrite(pin, 240)

async def main(pin):
    # use 'GPIO naming'
    wiringpi.wiringPiSetupGpio()
    
    # set #13 to be a PWM output
    wiringpi.pinMode(pin, wiringpi.GPIO.PWM_OUTPUT)
    
    # set the PWM mode to milliseconds stype
    #wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
    
    # divide down clock
    #wiringpi.pwmSetClock(192)
    #wiringpi.pwmSetRange(2000)
    
    try:
        while True:
            armBack(pin)
            await asyncio.sleep(1)
            armUp(pin)
            await asyncio.sleep(1)
            armDown(pin)
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        armBack(pin)

async def main2(pin):
    arm = Servo(pin, enable=True)
    try:
        while True:
            await arm.wave(1)
            await asyncio.sleep(2)
    except KeyboardInterrupt:
        arm.armUp()


# Main program logic follows:
if __name__ == '__main__':
    # must be run as root
    #if not os.geteuid() == 0:
    #    sys.exit('This script must be run as root in order to control the servo.')

    parser = argparse.ArgumentParser()
    parser.add_argument('--pin', type=int, help='BCM PIN number the servo is attached to', default=13)
    args = parser.parse_args()

    asyncio.get_event_loop().run_until_complete(main(args.pin))
