import RPi.GPIO as GPIO
import time

# Define motor driver pins
AIN1 = 13   # Direction pin
AIN2 = 19   # PWM pin for motor speed control

# Define encoder pins
ENC_A = 17
ENC_B = 4

# Initialize encoder counter
encoder_count = 0

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(ENC_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENC_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up PWM
pwm = GPIO.PWM(AIN2, 1000)  # 1 kHz frequency
pwm.start(0)

def encoder_callback(channel):
    global encoder_count
    if GPIO.input(ENC_B) == GPIO.input(ENC_A):
        encoder_count += 1
    else:
        encoder_count -= 1

# Attach interrupt to encoder
GPIO.add_event_detect(ENC_A, GPIO.RISING, callback=encoder_callback)

def set_motor(speed):
    """Sets motor speed and direction."""
    if speed > 0:
        GPIO.output(AIN1, GPIO.HIGH) #High is forward
    else:
        GPIO.output(AIN1, GPIO.LOW)  #Low is backwards
    pwm.ChangeDutyCycle(abs(speed))

try:
    while True:
        set_motor(50)  # Set speed to 50% duty cycle. Positive values are forwards.
        time.sleep(2)
        set_motor(-50)  # Reverse direction. Negative input is backwards.
        time.sleep(2)
        print(f"Encoder Count: {encoder_count}") #Outputs the position of the motors.
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()

#Everyone say "thank you, ChatGPT!"