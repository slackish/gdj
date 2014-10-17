#!/usr/bin/env python2.7

import os
import sys

from bottle import route, run, template, static_file

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

#run(host='localhost', port=8080, server="paste")
run(host='localhost', port=8080)
