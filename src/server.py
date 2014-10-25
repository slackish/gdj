#!/usr/bin/env python2.7

import ConfigParser
import os
import random
import sys
import time

from bottle import route, run, template, static_file

PICS = []
STARTTIME = 0
INTERVAL = 30

@route('/')
def main():
    """ returns main page with most JS magic """ 
    return template("main")

@route('/next')
def next():
    """ figure out next gif to return """
    return None


@route('/static/<path:path>')
def static(path):
    print >>sys.stderr, os.path.join("./static", path)
    return static_file(path, root="./static")


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


def load_config():
    """
    initializes the player
    """
    
    global STARTTIME, PICS

    config = ConfigParser.RawConfigParser()
    config.read("gdj.cfg")
    modules = config.get('gdj', 'modules')
    modules = [x.strip() for x in modules.split(",")]

    for module in modules:
        load_module(PICS, module)
    random.shuffle(PICS)
    STARTTIME = (int(time.time())/30) * 30



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


#run(host='localhost', port=8080, server="paste")
load_config()
run(host='localhost', port=8080)
