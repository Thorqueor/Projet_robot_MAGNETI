import RPi.GPIO as GPIO
import time


class Magnet:
    """This class was created to control Nicadrone magnets type R5C with a PWM
    signal emitted from the GPIO of a raspberry pi"""

    def Turn_ON(self):
        self.p.start(self.ON_duty_cycle)
        time.sleep(5) #Adjust this according to how much time the magnet takes to turn on.
        p.stop()

    def Turn_OFF(self):
        self.p.start(self.OFF_duty_cycle)
        time.sleep(5) #Adjust this according to how much time the magnet takes to turn on.
        p.stop()

    def destroy(self):
        """THIS METHOD MUST BE USED AT THE END OF YOUR PROGRAM IN ORDER TO PROPERLY RESET THE GPIOS USED
        DO NOT QUIT A PROGRAM WITHOUT CALLING THIS METHOD"""
        GPIO.cleanup()


    def __init__(self, pin_number, freq=None):
        """
        pin_number : The number of the GPIO pin that is used to send the pwm signal
        fre : the frequency used for the signal, per default it's fixed to 25 Hz according to the specifications of the magnet.
        """
        self.pin_number = pin_number
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_number, GPIO.OUT)

        if self.freq is None :
            self.freq = 25.0 #Hz
        self.period = 1.0/freq
        self.ON_pulse = (1.75 + 2.5)/(2.0*1000.0) #in seconds
        self.OFF_pulse = (0.5 + 1.25)/(2.0*1000.0) #in seconds
        self.ON_duty_cycle = 100*(1.0 - ON_pulse / period) #In our case the signal is inversed, see the electrical plan for more info.
        self.OFF_duty_cycle = 100*(1.0- OFF_pulse / period)
        self.p = GPIO.PWM(self.pin_number,self.freq)
