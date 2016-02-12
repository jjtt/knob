#!/usr/bin/python
# -*- coding: utf-8 -*-

import evdev
import sys

def printDevices():
  devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
  for device in devices:
    print(device.fn, device.name, device.phys)

def main(argv=None):
  if argv is None:
    argv = sys.argv

  if len(argv) != 2:
    print("input device missing")
    printDevices()
    return

  devicePath = argv[1]

  device = evdev.InputDevice(devicePath)

  preveventtime = 0
  preveventtype = None

  for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
      keyevent = evdev.categorize(event)
      if keyevent.keystate == keyevent.key_up:
        time = keyevent.event.timestamp()

        double = False
        if time - preveventtime < 0.2 and keyevent.keycode == preveventtype:
          double = True

        preveventtime = time
        preveventtype = keyevent.keycode

        if double:
          if keyevent.keycode == "KEY_VOLUMEUP":
            print("next")
          elif keyevent.keycode == "KEY_VOLUMEDOWN":
            print("prev")
        else:
          if keyevent.keycode == "KEY_VOLUMEUP":
            print("play")
          elif keyevent.keycode == "KEY_VOLUMEDOWN":
            print("pause")



if __name__ == "__main__":
  main()

