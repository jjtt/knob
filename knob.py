#!/usr/bin/python
# -*- coding: utf-8 -*-

import evdev
import sys
import time
import threading
import subprocess

SINGLE=False
DOUBLE=False
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
  global DOUBLE
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
      elif DOUBLE:
        if WHAT=='KEY_VOLUMEUP':
          mpc('next')
        elif WHAT=='KEY_VOLUMEDOWN':
          mpc('prev')
        DOUBLE=False

    next_call = next_call + 0.5
    time.sleep(next_call - time.time())


def main(argv=None):
  global SINGLE
  global DOUBLE
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

  for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
      keyevent = evdev.categorize(event)

      if keyevent.keystate == keyevent.key_up:

        time = keyevent.event.timestamp()

        WHAT = keyevent.keycode

        if time - PREVTIME < 0.2 and WHAT == preveventtype:
          SINGLE = False
          DOUBLE = True
        else:
          SINGLE = True
          DOUBLE = False

        PREVTIME = time
        preveventtype = WHAT




if __name__ == "__main__":
  main()

