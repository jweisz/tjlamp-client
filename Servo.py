import wiringpi
import asyncio

class Servo():
    def __init__(self, pin=13, enable=True):
        print(f"💪 initializing servo pin {pin} (enabled: {enable})")

        self.pin = pin
        self.enable = enable

        if not self.enable:
            return
        
        # use 'GPIO naming'
        wiringpi.wiringPiSetupGpio()
        
        # set #13 to be a PWM output
        wiringpi.pinMode(pin, wiringpi.GPIO.PWM_OUTPUT)
        
        # set the PWM mode to milliseconds stype
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
        
        # divide down clock
        wiringpi.pwmSetClock(192)
        wiringpi.pwmSetRange(2000)
    
    def armBack(self):
        if not self.enable:
            print(f"❌ suppressing armBack(), enable is False")
            return
        wiringpi.pwmWrite(self.pin, 60)

    def armUp(self):
        if not self.enable:
            print(f"❌ suppressing armUp(), enable is False")
            return
        wiringpi.pwmWrite(self.pin, 140)

    def armDown(self):
        if not self.enable:
            print(f"❌ suppressing armDown(), enable is False")
            return
        wiringpi.pwmWrite(self.pin, 240)

    async def wave(self, count):
        if not self.enable:
            print(f"❌ suppressing wave(), enable is False")
            return
        for _ in range(count):
            self.armUp()
            await asyncio.sleep(0.2)
            self.armDown()
            await asyncio.sleep(0.2)
            self.armUp()
            await asyncio.sleep(0.2)
