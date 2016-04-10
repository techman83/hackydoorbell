#!/usr/bin/python3

# Hacky Doorbell Daemon - Leon Wright - techman83@gmail.com - 2016-04-09
#
# Credits
# Button Example: http://razzpisampler.oreilly.com/ch07.html
# Noise Example: https://raspberrypikid.wordpress.com/2014/03/31/raspberry-pi-buzzer/

import configparser
import RPi.GPIO as GPIO
import time
import logging
import http.client
import urllib

# Main path
main_path = '/opt/doorbell'

# Configure Raspberry Pi Bits
buzzer_pin = 17
switch_pin = 18
blink_pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(blink_pin, GPIO.OUT)

# Configuration
config = configparser.RawConfigParser()
config.read(main_path + "/.pushover")
user_key = config.get('pushover','user_key')
app_key = config.get('pushover','app_key')

# logging
logger = logging.getLogger("Doorbell")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(main_path + "/doorbell.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

def send_message():
  try:
    logger.debug("Sending Pushover Message")
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": app_key,
        "user": user_key,
        "message": "Someone's at the door",
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
  except:
    logger.warn("The message failed to send")

def buzz():
  logger.debug("Buzzing")
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
  logger.debug("Blinking")
  for i in range(10):
    GPIO.output(blink_pin, True)
    time.sleep(0.05)
    GPIO.output(blink_pin, False)
    time.sleep(0.05)

def read_loop():
  logger.debug("Starting main loop")
  while True:
    input_state = GPIO.input(switch_pin)
    if input_state == False:
      logger.info('Doorbell Pressed')
      send_message()
      blink()
      buzz()
      time.sleep(5)

read_loop()
