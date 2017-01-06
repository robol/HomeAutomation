import json, requests

class Client():
    """A client of the Automation Server. """

    def __init__(self, name, address, port):
        self.__name = name
        self.__address = address
        self.__port = port

        self.__description = None
        self.__actions     = None

    def toJSON(self):
        return json.dumps({
            'name': self.__name,
            'address': self.__address,
            'port': self.__port
        })

    def cacheData(self):
        status = self.status()        
        self.__description = status['description']
        r = requests.get(self.__build_url('list-actions'))
        self.__actions = json.loads(r.text)

    def name(self):
        return self.__name

    def address(self):
        return self.__address

    def port(self):
        return self.__port

    def __str__(self):
        return "Client %s at %s on port %d" % (self.__name,
                                               self.__address,
                                               self.__port)

    def __build_url(self, page):
        return "http://%s:%s/%s" % (self.__address, self.__port, page)

    def status(self):
        r = requests.get(self.__build_url('status'))
        return json.loads(r.text)

    def ping(self):
        status = self.status()
        return status["status"] == "online"

    def doAction(self, data):
        r = requests.post(self.__build_url('action'),
                          json.dumps({ 'action': data }))
        return r.status_code == 200

    def getDescription(self):
        if self.__description is None:
            status = self.status()
            self.__description = status["description"]
        return self.__description

    def listActions(self):
        if self.__actions is None:            
            self.cacheData()

        return self.__actions
                                    
    
