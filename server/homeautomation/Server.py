#
# -*- coding: utf-8 -*-
#
# Author: Leonardo Robol <leo@robol.it>

import socket, threading, struct
from homeautomation.Utils import Logger
from homeautomation.Client import Client
from homeautomation.WebInterface import app

import zeroconf

class Server:

    def __init__(self):
        # The list of clients is initially empty, and will be popuplated
        # using the schedule and the multicast. 
        self.__clients = {}

    def listen(self, address, port):
        self.__discovery_service = ClientDiscoveryService()
        self.__discovery_service.start(
            lambda client : self.registerClient(client),
            lambda client : self.removeClient(client))

        # start the web interface
        self.__web_interface = app
        app.home_automation = self
        self.__web_interface.run(address, port)

    def clients(self):
        return self.__clients.values()

    def getClient(self, name):
        if name in self.__clients:
            return self.__clients[name]

    def clientAddresses(self):
        return list(map(lambda x : x.address(), self.__clients))

    def registerClient(self, client):
        Logger.logDebug('Registering new client: %s' % client)
        self.__clients[client.name()] = client

    def removeClient(self, name):
        if name in self.__client:
            Logger.logDebug('Deregistering client: %s' % name)
            self.__client.pop(name)
        else:
            Logger.logDebug('Cannot find a client that deregistered: %s' % name) 

class ClientDiscoveryService():

    def __init__(self):
        self.__zc = zeroconf.Zeroconf()
        
    def start(self, add_handler, remove_handler):
        self.__add_handler = add_handler
        self.__remove_handler = remove_handler
        zeroconf.ServiceBrowser(self.__zc, "_shap._tcp.local.", self)

    def close(self):
        self.__zc.close()

    def add_service(self, zc, type, name):
        info = self.__zc.get_service_info(type, name)

        client = Client(name,
                        socket.inet_ntoa(info.address),
                        info.port)
        client.cacheData()    
        self.__add_handler(client)

    def remove_service(self, zc, type, name):
        self.__remove_handler(name)
