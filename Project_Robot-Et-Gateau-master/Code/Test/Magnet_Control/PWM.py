#ssh pi@10.0.0.1
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

freq = 25.0 # Hz
period = 1.0/freq #s
chanel = 12
ON_pulse = (1.75 + 2.5)/(2.0*1000.0) #s
ON_duty_cycle = 100*(1.0 - ON_pulse / period )
OFF_pulse = (0.5 + 1.25)/(2.0*1000.0) #s
OFF_duty_cycle = 100*(1.0- OFF_pulse / period )
p = GPIO.PWM(chanel, freq)
#p.start( ON_duty_cycle )
p.start(OFF_duty_cycle )
time.sleep(6)
p.stop()
# p.ChangeDutyCicle( OFF_duty_cycle )
GPIO.cleanup()
~
~
~
