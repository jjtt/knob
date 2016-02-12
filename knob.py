#!/usr/bin/python
# -*- coding: utf-8 -*-

import evdev
import sys

def main(argv=None):
  if argv is None:
    argv = sys.argv

  if len(argv) != 2:
    print("input device missing")
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
      print(device.fn, device.name, device.phys)
    return

  devicePath = argv[1]

  device = evdev.InputDevice(devicePath)

  for event in device.read_loop():
    print(evdev.categorize(event))



if __name__ == "__main__":
  main()

