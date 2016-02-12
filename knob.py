#!/usr/bin/python
# -*- coding: utf-8 -*-

import evdev
import sys

def main(argv=None):
  if argv is None:
    argv = sys.argv

  if len(argv) != 1:
    print("input device missing")
    return

  print("todo")



if __name__ == "__main__":
  main()

