#
# -*- coding: utf-8 -*-
#
# Author: Leonardo Robol <leo@robol.it>

class IrrigationAction():

    def __init__(self, client, length):
        self.__client = client
        self.__length = length

    def trigger(self):
        """Connect to the client and trigger the Action. """
        pass

        
