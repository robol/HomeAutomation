#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from homeautomation import server

if __name__ == "__main__":
	server.listen('0.0.0.0', 9999, debug = True)
