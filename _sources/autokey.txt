.. Documentation of all functionality related to sending keystrokes

AutoKey Functionality - Sending Data to EOL
***********************************************

EOL AutoKey's method of putting its data into a format ETC consoles can understand relies on
sending virtual keystrokes to Expression Off-Line. This is accomplished using the
:meth:`SendKeys <pywinauto.controls.HwndWrapper.HwndWrapper.TypeKeys>` functionality of
:mod:`pywinauto.application`. Because of this, pywinauto is required to write data.

The :mod:`sender` Module
===============================================

.. module:: sender
   :synopsis: Uses pywinauto to send virtual keystrokes to EOL.
   :platform: Windows

The :mod:`sender` module provides the functionality that actually sends keys to Expression
Off-Line. :mod:`pywinauto` is initialized once, when the module is first loaded, at which
point it will attempt to find an Expression Off-Line window. If it fails then,
:mod:`pywinauto.findwindows` will throw a :exc:`WindowNotFoundError`, and the module will fail
to load. Once the module has been loaded, there is no way to reinitialize it without reloading
it completely.

.. Note:: This module is not written very well at the moment, so its implementation is likely
	  to change and improve.
	  
The :mod:`sender` module provides one function, which is used internally by most of the rest
of the software, especially :mod:`entities`.

.. autofunction:: send

The :mod:`keys` Module
=============================================

.. module:: keys
   :synopsis: Helps in converting various objects to SendKeys-compatible keystroke sequences.
   :platform: Windows

Technically the :mod:`keys` module is platform-independent, but it is not terribly useful except
to provide keystroke sequences for :meth:`~sender.send`, which is not, so it is marked as
Windows-only.

The :mod:`keys` module's central functionality is :data:`keys.names`, its :class:`KeyMap`, but
it also provides some :ref:`higher-level-functionality` that uses that :class:`KeyMap`.

Module Internals
--------------------------------------------

It is unlikely that you would need to create a new :class:`KeyMap`, but it is still documented
here because it provides a small API that may be useful occasionally.

.. class:: KeyMap (dict)

   A :class:`KeyMap` is a dictionary mapping names to
   :meth:`SendKeys <pywinauto.controls.HwndWrapper.HwndWrapper.TypeKeys>`\ -compatible keystrings
   or key sequences. It may map multiple names to the same key.

   In addition to the dictionary interface provided, it defines three methods which should be
   used to add additional mappings:

   .. automethod:: addkeys

   .. automethod:: addkey

   .. automethod:: addseq

      Examples from the :mod:`keys` module:

      .. literalinclude:: /../keys.py
	 :start-after: ### Built-In Sequences
	 :end-before: def 

.. data:: names

   This :class:`KeyMap` is the central dictionary mapping names to keys. It is used by the
   functions in this module to convert human-readable data to key sequences, and it also
   supports adding additional custom key sequences.

   It is initialized with one or more names for every keyboard shortcut EOL supports, as well
   as the above :meth:`~KeyMap.addseq` examples. [For more information, see
   :ref:`default-names-content`\ ]

   Because of the way the higher-level functions in the :mod:`keys` module work, all of the
   names in :data:`keys.names` should be lowercase and without spaces. This is explained more
   in the function descriptions for :func:`get` and :func:`parse_str`.

.. _higher-level-functionality:

Higher Level Functionality
----------------------------------------------

These functions provide higher-level access to :data:`keys.names`.

.. autofunction:: get

.. autofunction:: list_to_str

.. autofunction:: parse_str

.. _default-names-content:

Default Contents of :data:`keys.names`
--------------------------------------------------------

The following code adds all of the keyboard shortcuts Expression Off-Line supports.
Most keys have multiple names, for convenience, but all at least have the name of the physical
button you would press to get the same functionality.

.. literalinclude:: /../keys.py
   :start-after: names = KeyMap()
   :end-before: ### Softkeys
   :language: python

The :term:`softkey`\ s were added in a slightly different way, and can be access via `"softkey#"`,
`"soft#"`, or `"s#"`.

.. literalinclude:: /../keys.py
   :start-after: ### Softkeys
   :end-before: ### Built-In Sequences

In addition to these, the examples for :meth:`~KeyMap.addseq` are included.
