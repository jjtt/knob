#!/usr/bin/python
# -*- coding: utf-8 -*-

import evdev
import sys
import time
import threading
import subprocess

SINGLE=False
MANY=False
WHAT=None
PREVTIME=0

def printDevices():
  devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
  for device in devices:
    print(device.fn, device.name, device.phys)

def mpc(command):
  subprocess.call(['/usr/bin/mpc', command])

def timer():
  global SINGLE
  global MANY
  global WHAT
  global PREVTIME
  next_call = time.time()
  while True:
    if time.time() - PREVTIME > 0.2:
      if SINGLE:
        if WHAT=='KEY_VOLUMEUP':
          mpc('play')
        elif WHAT=='KEY_VOLUMEDOWN':
          mpc('pause')
        SINGLE=False
      elif MANY:
        if WHAT=='KEY_VOLUMEUP':
          mpc('next')
        elif WHAT=='KEY_VOLUMEDOWN':
          mpc('prev')
        MANY=False

    next_call = next_call + 0.5
    sleep_time = next_call - time.time()
    if sleep_time < 0:
      sleep_time = 0
    time.sleep(sleep_time)


def main(argv=None):
  global SINGLE
  global MANY
  global WHAT
  global PREVTIME

  if argv is None:
    argv = sys.argv

  if len(argv) != 2:
    print("input device missing")
    printDevices()
    return

  timerThread = threading.Thread(target=timer)
  timerThread.daemon = True
  timerThread.start()

  devicePath = argv[1]

  device = evdev.InputDevice(devicePath)

  preveventtype = None

  counter = 0

  for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
      keyevent = evdev.categorize(event)

      if keyevent.keystate == keyevent.key_up:

        if SINGLE == False and MANY == False:
          # Timer has handled the recognized event. Reset.
          counter = 0
          preveventtype = None

        time = keyevent.event.timestamp()

        WHAT = keyevent.keycode

        if time - PREVTIME < 0.2 and WHAT == preveventtype:
          counter += 1
          if counter > 3:
            SINGLE = False
            MANY = True
        else:
          counter = 0
          SINGLE = True
          MANY = False

        PREVTIME = time
        preveventtype = WHAT




if __name__ == "__main__":
  main()

