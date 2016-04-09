#!/usr/bin/python

# Hacky Doorbell Daemon - Leon Wright - techman83@gmail.com - 2016-04-09
#
# Credits
# Button Example: http://razzpisampler.oreilly.com/ch07.html
# Noise Example: https://raspberrypikid.wordpress.com/2014/03/31/raspberry-pi-buzzer/

import pushover
import os
import RPi.GPIO as GPIO
import time
import daemon
import lockfile

# Configure Raspberry Pi Bits
buzzer_pin = 17
switch_pin = 18
blink_pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(blink_pin, GPIO.OUT)

# Configure pushover client
client = pushover.PushoverClient(os.environ['HOME'] + "/.pushover")

# Configure Daemon

def send_message():
  try:
    client.send_message("Someone's at the door!")
  except SomeError:
    print "The message failed to send"
  return;

def buzz():
  pitch = 300
  period = 1.0 / pitch
  delay = period / 2
  cycles = int(2 * pitch)

  for i in range(cycles):
    GPIO.output(buzzer_pin, True)
    time.sleep(delay)
    GPIO.output(buzzer_pin, False)
    time.sleep(delay)

def blink():
  for i in range(10):
    GPIO.output(blink_pin, True)
    time.sleep(0.05)
    GPIO.output(blink_pin, False)
    time.sleep(0.05)

def read_loop():
  while True:
    input_state = GPIO.input(switch_pin)
    if input_state == False:
      print('Button Pressed')
      send_message()
      buzz()
      blink()
      time.sleep(5)

read_loop()
