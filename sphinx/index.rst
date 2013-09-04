.. PyLights documentation master file

PyLights
************************************

PyLights is a suite of python software for working with ETC consoles and
:term:`Expression Off-Line`. It provides a remote control server and client
that can interface with a console via MIDI and track the screen using
:term:`EOL`, as well as a history tracking feature allowing recall of the
console state at any give time. Additionally, it provides an object-oriented
python interface to light board entities, allowing you to script show creation
and editing and export nice custom representations of your show.

It has limited support for reading and writing ETC's files, and relies mainly
on sending keystrokes to :term:`Expression Off-Line` or MIDI messages to a
console to write most data.

I work with an ETC Express 48/96, so it has been optimized for that console.
However, it should work fine with other consoles in theory, although it may
not be able to read their showfiles or control everything.

Get the Code
====================================

The source code is available on github: https://github.com/baryon5/pylights

PyLights is designed to be compatible with both python 2.7 and >=3.2 whereever
possible. For this reason, `six <https://pypi.python.org/pypi/six/>`_ is bundled
at :mod:`pylights.libs.six`.


Sending commands to :term:`Expression Off-Line` requires several \*nix
programs/libraries to be installed:

* `Xvfb <http://www.x.org/archive/current/doc/man/man1/Xvfb.1.xhtml>`_
* `xdotool <http://www.semicomplete.com/projects/xdotool/>`_
* `wine <http://www.winehq.org/>`_

To install them on Ubuntu (or other debian-based systems), try::

  $ sudo apt-get install xvfb xdotool wine

Sending commands to a physical console is accomplished via MIDI using
`pygame <http://www.pygame.org/news.html>`_. Additionally, in order for
PyLight's sent commands to be recognized by the console, a showfile containing
several macros must be loaded.

Documentation
====================================

If you just want to set up a remote control server and client, read
:doc:`tutorial`.

.. toctree::
   :maxdepth: 3
   :glob:
   :numbered:

   tutorial
   daemon/*
   client/*
   entities/entities
   entities/*
