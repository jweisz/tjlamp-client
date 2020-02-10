import pigpio
import wiringpi
import asyncio

class ServoPigpio():
    def __init__(self, pin=13, enable=True):
        self.pin = pin
        self.enable = enable

        self.SERVO_BACK = 500
        self.SERVO_UP = 1400
        self.SERVO_DOWN = 2300

        if not self.enable:
            print("❌ servo disabled")
            return
        
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise Exception("pigpio unable to connect to pigpiod daemon. try running sudo pigpiod (or sudo systemctl enable pigpiod).")
    
    def armBack(self):
        if not self.enable:
            return
        self.pi.set_servo_pulsewidth(self.pin, self.SERVO_BACK)

    def armUp(self):
        if not self.enable:
            return
        self.pi.set_servo_pulsewidth(self.pin, self.SERVO_UP)

    def armDown(self):
        if not self.enable:
            return
        self.pi.set_servo_pulsewidth(self.pin, self.SERVO_DOWN)

    async def wave(self, count):
        if not self.enable:
            return
        for _ in range(count):
            self.armUp()
            await asyncio.sleep(0.2)
            self.armDown()
            await asyncio.sleep(0.2)
            self.armUp()
            await asyncio.sleep(0.2)

class ServoWiringPi():
    """Control the servo using WiringPi. Note that this conflicts with using the NeoPixels
    due to PWM issues, so our real Servo class will be based on pigpio (which somehow avoids
    the issue."""
    def __init__(self, pin=13, enable=True):
        print(f"💪 initializing servo pin {pin} (enabled: {enable})")

        self.pin = pin
        self.enable = enable

        if not self.enable:
            print("❌ servo disabled")
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
            return
        wiringpi.pwmWrite(self.pin, 60)

    def armUp(self):
        if not self.enable:
            return
        wiringpi.pwmWrite(self.pin, 140)

    def armDown(self):
        if not self.enable:
            return
        wiringpi.pwmWrite(self.pin, 240)

    async def wave(self, count):
        if not self.enable:
            return
        for _ in range(count):
            self.armUp()
            await asyncio.sleep(0.2)
            self.armDown()
            await asyncio.sleep(0.2)
            self.armUp()
            await asyncio.sleep(0.2)
