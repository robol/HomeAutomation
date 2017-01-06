#
# -*- coding: utf-8 -*-

from flask import Flask, send_from_directory, Response, render_template
import json
from homeautomation.Client import Client

def errorResponse(message):
    return JSONResponse({ 'error': message })

def json_convert(obj):
    try:
        return obj.toJSON()
    except:
        return json.dumps(obj)

def JSONResponse(obj):
    """Take a Python object and convert it to its JSON
    representation encoded in a Flask Response"""    
    json_rep = json.dumps(obj, default = json_convert) 
    return Response(json_rep,
                    mimetype = 'application/json')

app = Flask(__name__, static_url_path = '/static')
app.debug = True

@app.route('/')
def index():
    return render_template('index.html',
                           clients = app.home_automation.clients())

@app.route('/client/<name>')
def client(name):
    client = app.home_automation.getClient(name)
    if client is None:
        pass
    else:
        return render_template('client.html', client = client)

@app.route('/static/<path:path>')
def static_files():
    return send_from_directory('static', path)

@app.route('/clients')
def client_list():
    return Response(list(map(lambda x : x.toJSON(), app.home_automation.clients())))

@app.route('/client/<name>/action/<action>')
def client_action(name, action):
    client = app.home_automation.getClient(name)
    if client is not None:
        return JSONResponse(client.doAction(action))

@app.route('/client/<name>/description')
def client_description(name):
    client = app.home_automation.getClient(name)
    if client is not None:
        return JSONResponse(client.getDescription())
    else:
        return errorResponse('client not found')

@app.route('/client/<name>/status')
def client_status(name):
    client = app.home_automation.getClient(name)
    if client is not None:
        return JSONResponse(client.status())
    else:
        return errorResponse('client not found')


@app.route('/client/<name>/list-actions')
def client_list_actions(name):
    client = app.home_automation.getClient(name)
    if client is not None:
        return JSONResponse(client.listActions())
    else:
        return errorResponse('client not found')
    
    
