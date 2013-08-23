.. Documentation for the "etcfiles" package

Working with Console Files
****************************************

This software has limited support for reading and writing certain files used or created by
ETC consoles and software. Fixture Personalities may be completely read and written, and parts
of showfiles may be read (eventually...that's not implemented yet).


Working with ETC Showfiles
===================================================
**#TODO**

.. automodule: /Removed : to comment out/ etcfiles.shwfile
   :members:

Working with ETC Fixture Personalities
===================================================
.. module:: etcfiles.personality
   :synopsis: Allows you to use ETC's Fixture Personality files.

The :mod:`etcfiles.personality` module provides two public classes for working with Fixture
Personalities. Unlike :class:`etcfiles.shwfile.Showfile`, the :class:`Personality` class may
be read from and written to ETC personality files directly and should have no problems.

The :class:`Personality` and :class:`PChannel` classes support all of the data stored in a
personality file by the "Personality Editor", even though much of it may not be used by all
consoles. For that reason, for now, only the more common features are documented.

.. autoclass:: Personality

   No arguments need to be supplied when a :class:`Personality` is created, although they may be.
   If `channels` is supplied, it must be a sequence of :class:`PChannel`\ s.

   Alternatively, a personality may be loaded from a file by way of :meth:`from_file`.

   .. classmethod:: from_file(fn, writeable=True)

      Use this method to load a :class:`Personality` from an ETC personality file. `fn` is the
      filename to load from, and `writeable` controls whether the filename will be remembered.

      For a little more explanation, see :meth:`etcfiles.Readable.from_file`.

   .. method:: write(fn=None)

      Saves the personality in the ETC format to the specified file. If `fn` is `None` and the
      filename used with :meth:`from_file` was remembered, it will use that filename.

   These attributes are the fields in an ETC personality:

   .. attribute:: label

      This must be a string no longer than twelve characters. Attempting to set this to a longer
      string will result in a :exc:`ValueError`.

   .. attribute:: remote_dimmer

      This must be a boolean value, and will result in a :exc:`ValueError` if you attempt to set
      it otherwise.

   .. attribute:: channels

      A special sequence object acting partially as a list of :class:`PChannel` objects
      representing each channel/dimmer defined by the personality. If it is assigned to, it must
      be assigned a sequence of :class:`PChannel`\ s.

      You may retrieve individual :class:`PChannel` objects from the list using index notation::
	>>> p.channels[0] # Returns the first channel of p
      However, you may not assign new :class:`PChannel`\ s. Instead, use :meth:`channels.add` to
      replace channels (see its documentation).

   Channels may be added to a personality through its :meth:`addChannel` method, or its
   :meth:`channels.add` method. To replace existing channels, simply create a new one with the
   same :attr:`PChannel.dimmer` value as an existing one and add it using either of these methods,
   and it will replace the existing one.

   .. automethod:: addChannel

      This method will create a new :class:`PChannel` for you with whatever options you specify
      and add it to :attr:`channels`. If you specify a `dimmer`, it will create the new
      :class:`PChannel` at that position, overwriting any that may have previously been there.
      If you do not specify a dimmer, it will just add this channel at the end, after the
      currently last channel.

      It will accept either a string or an integer for `atype`. If it does not get an integer,
      it will perform a lookup of the string in :data:`_attribute_types` to determine its
      integer value.

      Any additional arguments passed to :meth:`addChannel` are just passed on to the
      :class:`PChannel` constructor.

   .. method:: channels.add(channel)

      This method takes an already-instantiated :class:`PChannel` object and adds it to
      :attr:`channels` at whatever position is specified by :attr:`PChannel.dimmer` for that
      channel, overwriting any that may already have been there. Any attempts to add
      non-:class:`PChannel` objects will raise a :exc:`TypeError`.

      If a :class:`PChannel` is added with a dimmer beyond the length of the :attr:`channels`
      list, blank :class:`PChannel` objects are created to fill in the space between the current
      last channel and the dimmer position of the new one. The :attr:`PChannel.atype` of these
      objects is 0, or "Not Used".

.. autoclass:: PChannel


The :mod:`etcfiles.personality` module provides two module level constants to assist in
generating nicer representations of the data stored in a personality. They are mainly used
internally, but are documented here anyway. They are each lists, since they only need to map
a contiguous set of integers starting at 0, for which list indices work fine.

.. data:: _attribute_types

   This is ETC's list of personality channel types, and is used internally to map type names
   to integers and vice-versa.

.. data:: _display_types

   This maps the integers used to represent different channel "display types" to strings.
   There are only four of them.


Adding Binary File IO Support to Custom Classes
===================================================
.. module:: etcfiles
   :synopsis: Provides functionality for representing and working with objects
      stored in binary files created by ETC software.

.. Note:: These classes are used by the modules of the etcfiles package and probably have no
	  external use, so they are just documented here because they can be!

The base :mod:`etcfiles` module contains base classes that implement some binary
file IO. These can be inherited to use their functionality in custom classes. To make a class
readable, inherit :class:`Readable`. To make a class writeable, inherit :class:`Writeable`.
You may use any combination of the two classes, so a class can be readable and writeable,
or even just writeable.

.. Note:: *Only for Python 2.x*: Any class that inherits from :class:`Readable` or
   :class:`Writeable` is automatically a new-style class, as they both inherit from `object`.

.. class:: Readable

   To make a class readable, inherit from the :class:`Readable` class. This will provide
   your class with two classmethods, :meth:`from_string` and :meth:`from_file`.
   
   However, in order to actually make a class readable or writeable, it must define (at least)
   :attr:`_struct_format` and :attr:`_struct_fields` at the class level.


   .. attribute:: _struct_format

      A :mod:`struct` format string, it will be passed to :func:`struct.unpack` when parsing
      the file.

   .. attribute:: _struct_fields

      A sequence defining how the objects returned from unpacking the binary data will be passed
      to the constructor. It should contain the name of the argument each field should be passed
      to the constructor as as strings, and `None` for fields that should be ignored.

      If a field name appears multiple times, the field will passed to your constructor as a
      list containing all fields with that name.

      .. _recursive_struct_packing:

      **Recursive Field Parsing:**

      Additionally, for fields which should further be parsed into custom objects, place a `*`
      in front of the field name, and define :attr:`_struct_structs`. Any field in
      :attr:`_struct_fields` which is preceded by a `*` will be looked up in
      :attr:`_struct_structs`, and the :meth:`from_string` constructor of the specified class
      will be called on the field's value before it is used to construct a new object.

      .. Note:: This is used by :class:`Writeable` objects as well to properly format null
		fields and recursively pack objects.

   .. attribute:: _struct_structs

      A dictionary mapping field names (without the `*`) to custom classes (which must in turn
      be :class:`Readable`).

   Inheriting the :class:`Readable` class provides your class with two classmethods that can be
   used to create an instance from binary data.

   .. automethod:: from_string

      It will first attempt to construct a new object using its default constructor,
      passing in the fields using dictionary expansion. If that fails because the method
      signature does not match, it will attempt to use the :meth:`from_struct` classmethod of
      the class, passing in the same arguments. This allows you to have a constructor with a
      signature that is incompatible with the binary format.

      .. Note:: This method is also used internally when recursively parsing objects.

   .. automethod:: from_file

   .. classmethod:: from_struct(**args)

      If your constructor has a signature that is incompatible with the binary format/fields
      as defined in :attr:`_struct_fields`, you must write a :meth:`from_struct` classmethod.
      :meth:`from_struct` will still be called the same way as your constructor, using a
      dictionary expansion of the fields specified in :attr:`_struct_fields` and their values.

      .. Warning:: This method is NOT defined by :class:`Readable`!

.. class:: Writeable

   This class functions very much like :class:`Readable`, with a few notable differences:

   1. :attr:`Readable._struct_fields` is not required to write an object. It is still useful,
      however, to easily write null fields, and if you want
      :ref:`recursive object packing <recursive_struct_packing>` you must define it.
   2. :attr:`Readable._struct_structs` is unnecessary even if you are using
      :ref:`recursive object packing <recursive_struct_packing>`, because :meth:`to_string`
      just calls object's :meth:`to_string` methods. This means that subobjects must still be
      :class:`Writeable`.
   3. :meth:`Readable.from_struct` is, of course, never necessary, but a new method,
      :meth:`to_struct`, must be defined.

   Like :class:`Readable`, :class:`Writeable` defines two methods for binary IO, :meth:`to_string`
   and :meth:`write`.

   .. automethod:: to_string

      This method will call the object's :meth:`to_struct` method to get a list of field data.
      It expects a sequence of data suitable for packing into a :mod:`struct`, although if
      specified in :attr:`Readable._struct_fields` certain fields will be :ref:`recursively packed <recursive_struct_packing>`.

   .. automethod:: write

   In order to make a class properly writeable, you must define a :meth:`to_struct` method:

   .. method:: to_struct()

      You must provide this method to make a class writeable. It is given no arguments and should
      return a sequence of fields to be packed. Any non integer/string fields (depending on your
      format string) must correspond with `*`-marked fields in :attr:`Readable._struct_fields`.

      .. Warning:: This method is NOT defined by :class:`Writeable`!
