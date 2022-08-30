import RPi.GPIO as GPIO 
import time 
import keyboard

def setup():
  # first stepper motor
  # clear disk
  PUL_1 = 11
  DIR_1 = 13    
  ENA_1 = 15
  control_pins_1 = [11, 13, 15]
  # set pins 1
  for pin in control_pins_1:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
  # second stepper motor
  # yellow disk
  PUL_2 = 16
  DIR_2 = 18
  ENA_2 = 22
  control_pins_2 = [16, 18, 22]
  # set pins 2
  for pin in control_pins_2:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
    GPIO.setmode(GPIO.BOARD)
  print("Initialization of pins complete.\n")
  return [control_pins_1, control_pins_2]


def protocol_1(pins):
  #pins
  control_pins_1 = pins[0]
  control_pins_2 = pins[1]
  #experimental parameters
  direction = raw_input("Please enter the direction in which you want the platform to turn.\n CW for clockwise and CCW for counterclockwise: ")
  print("\n")
  steps = 3200
  trials = int(raw_input("Please enter the number of trials you want to perform as an integer: "))
  print("\n")
  pause = int(raw_input("Please enter the pause you want between each trial as an integer in seconds: "))
  print("\n")
  delay = 0.001
  # default pin setting
  GPIO.output(control_pins_1[2], GPIO.HIGH)
  time.sleep(0.5)
  GPIO.output(control_pins_2[2], GPIO.HIGH)
  time.sleep(0.5)
  print('ENA set to HIGH - Controller Enabled\n')
  GPIO.output(control_pins_2[1], GPIO.LOW)
  if direction == 'CW':
    GPIO.output(control_pins_1[1], GPIO.LOW)
  else:
    GPIO.output(control_pins_1[1], GPIO.HIGH)
  print('DIR set - Direction Enabled\n')
  #start experiment
  for n in range(trials*2):
    for step in range(steps):
      GPIO.output(control_pins_1[0], GPIO.HIGH)
      time.sleep(delay)
      GPIO.output(control_pins_1[0], GPIO.LOW)
      time.sleep(delay)
    time.sleep(1)  
    if n % 1 == 0: #n % 2 == 0:
      print("Trial #" + str(n/2 + 1))
      print("\n")
      for step in range(100):
        GPIO.output(control_pins_2[0], GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(control_pins_2[0], GPIO.LOW)
        time.sleep(delay)
    time.sleep(pause)
  else:
    time.sleep(pause)
  GPIO.output(control_pins_1[2], GPIO.LOW)
  time.sleep(0.5)
  GPIO.output(control_pins_2[2], GPIO.LOW)
  time.sleep(0.5)
  print('ENA set to LOW - Controller Disabled\n')
  GPIO.cleanup()
  return


def protocol_2(pins):
  #pins
  control_pins_1 = pins[0]
  control_pins_2 = pins[1]
  #experimental parameters
  direction = raw_input("Please enter the direction in which you want the platform to turn.\n CW for clockwise and CCW for counterclockwise: ")
  print("\n")
  steps = 1280
  trials = int(raw_input("Please enter the number of trials you want to perform as an integer: "))
  print("\n")
  pause = 2
  delays = [0.005, 0.0025, 0.001]
  speed = int(raw_input("Please enter the speed at which you want the tile to turn as an integer from 1 to 3.\n1 is the slowest speed and 3 is the highest speed: "))
  print("\n")
  delay = delays[speed-1]
  # default pin setting
  GPIO.output(control_pins_1[2], GPIO.HIGH)
  time.sleep(0.5)
  GPIO.output(control_pins_2[2], GPIO.HIGH)
  time.sleep(0.5)
  print('ENA set to HIGH - Controller Enabled\n')
  GPIO.output(control_pins_2[1], GPIO.LOW)
  if direction == 'CW':
    GPIO.output(control_pins_1[1], GPIO.LOW)
  else:
    GPIO.output(control_pins_1[1], GPIO.HIGH)
  print('DIR set - Direction Enabled\n')
  #start experiment
  for n in range(trials):
    print("Trial #" + str(n+1))
    print("\n")
    for step in range(steps):
      GPIO.output(control_pins_1[0], GPIO.HIGH)
      time.sleep(delay)
      GPIO.output(control_pins_1[0], GPIO.LOW)
      time.sleep(delay)
    for step in range(100):
      GPIO.output(control_pins_2[0], GPIO.HIGH)
      time.sleep(delay)
      GPIO.output(control_pins_2[0], GPIO.LOW)
      time.sleep(delay)
  GPIO.output(control_pins_1[2], GPIO.LOW)
  time.sleep(0.5)
  GPIO.output(control_pins_2[2], GPIO.LOW)
  time.sleep(0.5)
  print('ENA set to LOW - Controller Disabled\n')
  GPIO.cleanup()
  return


if __name__ == "__main__":
  GPIO.setmode(GPIO.BOARD)
  pins = setup()
  protocol = raw_input("Please enter the number of the protocol you wish to carry out.\n 1 for the normal paw reach and 2 for the timed paw reach: ")
  print("\n")
  if protocol == "1":
    protocol_1(pins)
  else:
    protocol_2(pins)
