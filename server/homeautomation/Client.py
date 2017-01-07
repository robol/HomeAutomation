import json, requests, simplejson

class Action():

    def __init__(self, name, description, parameters):
        """An Action that can be performed by a Client"""
        self.__name = name
        self.__description = description
        self.__parameters = parameters

    def parameterType(self, parameter_name):
        return self.__parameters[parameter_name]

    def parameters(self):
        return self.__parameters.keys()

    def name(self):
        return self.__name

    def description(self):
        return self.__description

class Property():

    def __init__(self, name, description):
        self.__name = name
        self.__description = description

    def name(self):
        return self.__name

    def description(self):
        return self.__description

class Client():
    """A client of the Automation Server. """

    def __init__(self, name, address, port):
        self.__name = name
        self.__address = address
        self.__port = port

        self.__description = None
        self.__actions     = None

        self.__online = False

    def toJSON(self):
        return json.dumps({
            'name': self.__name,
            'address': self.__address,
            'port': self.__port
        })

    def cacheData(self):
        self.__description = json.loads(self.__do_get('description'))["description"]

        # Load Actions
        self.__actions = []
        for action in json.loads(self.__do_get('list-actions')):
            description = action["description"]
            name = action["name"]
            parameters = {}
            if "parameters" in action:
                for p in action["parameters"]:
                    parts = p.split(":")
                    pname = parts[0]
                    if len(name) > 1:
                        ptype = parts[1]
                    else:
                        ptype = "string"
                    parameters[pname] = ptype
            self.__actions.append(Action(name, description, parameters))
            
        self.__properties = []
        for property in json.loads(self.__do_get('list-properties')):
            self.__properties.append(Property(property["name"], property["description"]))

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

    def __do_get(self, page):
        try:
            r = requests.get(self.__build_url(page))
            self.__online = True
            return r.text
        except requests.exceptions.Timeout:
            self.__online = False

    def __do_post(self, page, params):
        try:
            r = requests.post(self.__build_url(page), params)
            self.__online = True
            return r.text
        except requests.exceptions.Timeout:
            self.__online = False

    def status(self):
        status = json.loads(self.__do_get('status'))
        return status["status"]

    def ping(self):
        self.status()
        return self.__online

    def isOnline(self):
        return self.__online

    def doAction(self, action, params = None):
        if params is not None:
            params['action'] = action
        else:
            params = { 'action': action }
        return json.loads(self.__do_post('action',
                                         json.dumps(params)))

    def getDescription(self):
        if self.__description is None:
            self.cacheData()
        return self.__description

    def listActions(self):
        if self.__actions is None:            
            self.cacheData()

        return self.__actions

    def listProperties(self):
        if self.__properties is None:
            self.cacheData()

        return self.__properties
                                    
    
