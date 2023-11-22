import RPi.GPIO as GPIO
import time

# Sets the Pi so it knows we are using the physical pin numbering
GPIO.setmode(GPIO.BOARD)

# Sets up pin 18 as an input
GPIO.setup(24, GPIO.IN, GPIO.PUD_DOWN)

# Detects the button being pressed
def waitButton():
    print(GPIO.input(24))
    GPIO.wait_for_edge(24, GPIO.RISING)
    print(GPIO.input(24))
    print('Button pressed!')

# Runs function
waitButton()