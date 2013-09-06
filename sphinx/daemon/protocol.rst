.. The client/server command protocol

The Client/Server Protocol
*********************************

Every message must start with two bytes identifying its type and subtype (what
the heck is that?), followed by two bytes describing the length of the message
(not inluding that header). Given the 2 byte length header, the maximum size of
any message is 64 KB, but that should be way more than enough!

.. module:: pylights.daemon.protocol

How the message is interpreted and what it should contain depends on the specified
type.

Defined Message Types and Subtypes
======================================

`0x00 *`
   :ref:`meta-commands` - See below

`0x10 *`
   A raw string message

`0x12 [0x00 or 0x01]`
   A pre-processed command sequence. The subtype indicates how many bytes are used
   to describe each command, `0x00` if one byte per command, `0x01` if two.


.. _meta-commands:

Meta Commands
-------------------------------------

Messages whose type is `0x00` are special and pertain to controlling the core daemon,
not any modules, command processors, or extensions. As of now, none exist...
