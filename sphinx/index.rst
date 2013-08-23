.. EOL AutoKey documentation master file, created by
   sphinx-quickstart on Thu Aug 22 16:31:53 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EOL AutoKey
************************************

EOL AutoKey is a suite of python software to assist in making shows for ETC
consoles. It provides an object-oriented python interface to light board
entities, allowing you to script show creation and editing, or export nice
representations of your show.

It has limited support for reading and writing ETC's files, and relies mainly
on sending keystrokes to Expression Off-Line to write most data. For that
reason, in order to write show data, you must have a windows computer and be
able to run ETC's Expression Off-Line software.

I work with an ETC Express 48/96, so it has been optimized for that console.
However, it should work fine with other consoles supported by Expression
Off-Line, in theory, although it may not be able to read their showfiles.

Documentation
====================================

This documentation assumes you are familiar with an ETC console and related
concepts (and ideally Expression Off-Line as well), as it only explains how
those things relate to this python interface.

.. toctree::
   :maxdepth: 2

   autokey
   entities
   etcfiles
