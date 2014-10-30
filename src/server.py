#!/usr/bin/env python2.7

import ConfigParser
import os
import random
import sys
import time

from bottle import route, run, template, static_file

PICS = []
PICLEN = 0
STARTTIME = 0
INTERVAL = 20; 

#####################################################################
#
# Bottle Handlers
#
#####################################################################

@route('/')
def main():
    """ returns main page with most JS magic """ 
    return template("main")

@route('/next')
def next():
    """ figure out next gif to return """
    index, nexttime = whatsnext()
    return {'switchTime': str(nexttime), 
            'nextImg': PICS[index]}


@route('/static/<path:path>')
def static(path):
    print >>sys.stderr, os.path.join("./static", path)
    return static_file(path, root="./static")


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)
    
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
run(host='0.0.0.0', port=8080, server="paste")
#run(host='0.0.0.0', port=8080)
