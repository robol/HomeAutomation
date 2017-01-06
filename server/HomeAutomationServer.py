#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from homeautomation.Server import Server

if __name__ == "__main__":

    server = Server()
    server.listen('0.0.0.0', 9999)

    

    
