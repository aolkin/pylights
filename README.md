PyLights
===========

###### Python functionality for controlling and working with ETC lighting consoles

PyLights contains three packages, daemon, client, and entities.

PyLights is designed to be compatible with both python >=2.7 and 3.x.

#### The Daemon Package

The daemon package allows you to run a server that will forward commands to Expression Off-Line
or a physical console via MIDI. Only one of those options may be used, or they can be combined
for maximum usefulness.

Sending commands to Expression Off-Line requires several *nix programs to be installed:
- [Xvfb] (http://www.x.org/archive/current/doc/man/man1/Xvfb.1.xhtml)
- [xdotool] (http://www.semicomplete.com/projects/xdotool/)
- [wine] (http://www.winehq.org/)

To install them on Ubuntu (or other debian-based systems), try:

    sudo apt-get install xvfb xdotool wine

Sending commands to a physical console is accomplished via MIDI using
[pygame](http://www.pygame.org/news.html). Additionally, in order for PyLight's sent commands
to be recognized by the console, a showfile containing several macros must be loaded.

#### The Client Package

This package contains a command-line script for communicating with the daemon, as well as
a web server that provides a web interface to the daemon. A mobile app that uses that web
server to communicate with the daemon is also planned...

The web server will probably use [tornado](http://www.tornadoweb.org/en/stable/), though as
of now that is undecided.

#### The Entities Package

This package provides pythonic data structures for representing console entities.

### Documentation

The Makefile in the root directory of this project is for generating sphinx documentation,
not building any part of project code.

[Documentation for Latest Version] (http://eol-autokey.baryon5.tk/)
