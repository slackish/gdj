# GDJ #

Instead of video DJ (VDJ), this is GIF DJ (GDJ).

The idea here is to KISS, but semi-entertaining.


# How do I use this? #

Download some gifs, download the software, read the source, and go nuts.

Seriously, this isn't (and will likely never be) ready for production, so use 
at your own risk.

## Setup

    apt-get install libev-dev
    pip3 install gevent-websocket 
    pip3 install bottle

## Configuration

There are two pieces you will want to configure.  First one is the logo, which will always be src/static/logo.png.  Just overwrite it with whatever logo you have.

The second is to run through `src/gdj.cfg`.  The two primary settings are the
interval (seconds between each picture change) and modules (a commma separated
list of directories to populate for animated pictures).

## Running

    cd src
    python3 server.py
    

# Credits #

This awful system wouldn't of been possible without:

 * James Wernickie
