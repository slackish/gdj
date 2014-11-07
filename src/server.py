#!/usr/bin/env python2.7

import ConfigParser
import os
import random
import sys
import time

from bottle import route, run, template, static_file, abort, Bottle, request

PICS = []
PICLEN = 0
STARTTIME = 0
INTERVAL = 20; 

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
    print >>sys.stderr, os.path.join("./static", path)
    return static_file(path, root="./static")


@app.route('/admin')
def admin():
    return template("admin_landing")

@app.route('/websocket')
def ws():
    """
    websocket code
    """
    print >>sys.stderr, "websocket called"
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            print >>sys.stderr, "got a message!:", message
            wsock.send("1,Your message was: %r" % message)
        except WebSocketError:
            break

    
#####################################################################
#
# Bottle helpers
#
#####################################################################

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
    
    global STARTTIME, PICS, PICLEN

    config = ConfigParser.RawConfigParser()
    config.read("gdj.cfg")
    modules = config.get('gdj', 'modules')
    modules = [x.strip() for x in modules.split(",")]

    for module in modules:
        load_module(PICS, module)
    random.shuffle(PICS)

    PICLEN = len(PICS)

    STARTTIME = (int(time.time())/INTERVAL) * INTERVAL



def load_module(pics, module):
    """
    lets find all the pictures
    """
    moddir = os.path.join(".", "static", "imgs", module)
    if os.path.isdir(moddir):
        for f in os.listdir(moddir):
            if f.endswith(".gif") or f.endswith(".jpg"):
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
