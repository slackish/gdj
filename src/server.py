#!/usr/bin/env python2.7

import configparser
import os
import random
import sys
import time
import traceback

from bottle import route, run, template, static_file, abort, Bottle, request
from functools import reduce

PICS = []
PICLEN = 0
STARTTIME = 0

clients = []
current_message = ""
INTERVAL = 20; 
EXTENSIONS = (".gif", ".jpg", ".png")

#####################################################################
#
# Bottle Routing
#
#####################################################################
app = Bottle()

@app.route('/')
def main():
    """ returns main page with most JS magic """ 
    return template("main")

@app.route('/next')
def next():
    """ figure out next gif to return """
    index, nexttime = whatsnext()
    return {'switchTime': str(nexttime), 
            'nextImg': PICS[index]}


@app.route('/static/<path:path>')
def static(path):
    print(os.path.join("./static", path), file=sys.stderr)
    return static_file(path, root="./static")


@app.route('/admin')
def admin():
    return template("admin_landing")

@app.route('/admin/chat')
def admin():
    return template("admin_chat")

@app.route('/websocket')
def ws():
    """
    websocket code
    """
    print("websocket called", file=sys.stderr)
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    clients.append(wsock)

    while True:
        try:
            message = wsock.receive()
            if message != None:
                handle_ws(message, wsock)
            else:
                break
        except WebSocketError:
            break

    
#####################################################################
#
# Bottle helpers
#
#####################################################################


def handle_ws(message, ws):
    """
    fall through opcodes do do work
    """
    global current_message

    if "," in message:
        op, message = message.split(",", 1)
        op = int(op)
    elif message.strip().isdigit():
        op = int(message)
        message = ""
    else:
        print("WTF is '%s'" % str(message), file=sys.stderr)

    print("op %d, message: %s" % (op, message))

    if op == 0:
        ws.send("1,%s" % current_message)
    elif op == 1:
        print(clients, file=sys.stderr)
        current_message = message
        message = "1,%s" % message
        send_to_all_ws(message)
        

def send_to_all_ws(message):
    for s in clients[:]:
        try:
            s.send(message)
            print("sent 1")
        except WebSocketError:
            traceback.print_exc()
            clients.remove(s)


def whatsnext():
    """ based on the time, return the next index """
    index = (1 + int((time.time() - STARTTIME) / INTERVAL))
    nexttime = STARTTIME + (index * INTERVAL)
    index = index % PICLEN
    return (index, nexttime)
    


#####################################################################
#
# Initialization Code
#
#####################################################################


def load_config():
    """
    initializes the player
    """
    
    global INTERVAL, STARTTIME, PICS, PICLEN

    config = configparser.RawConfigParser()
    config.read("gdj.cfg")
    modules = config.get('gdj', 'modules')
    modules = [x.strip() for x in modules.split(",")]

    for module in modules:
        load_module(PICS, module)
    random.shuffle(PICS)

    PICLEN = len(PICS)

    INTERVAL = int(config.get('gdj', 'interval'))

    STARTTIME = (int(time.time())/INTERVAL) * INTERVAL



def load_module(pics, module):
    """
    lets find all the pictures
    """
    moddir = os.path.join(".", "static", "imgs", module)
    if os.path.isdir(moddir):
        for f in os.listdir(moddir):
            if reduce(lambda x,y: x or y, list(map(f.endswith, EXTENSIONS))):
                f = f.replace(" ", "%20")
                picpath = os.path.join(moddir[1:], f)
                pics.append(picpath)


load_config()
#run(host='0.0.0.0', port=8080, server="paste")
#run(host='0.0.0.0', port=8080)



from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
server = WSGIServer(("0.0.0.0", 8080), app,
                    handler_class=WebSocketHandler)
server.serve_forever()
