.. Documentation of basic "entity" support and built-in entities

Entities – Object-Oriented Interface to Console Data
*******************************************************

EOL AutoKey provides a framework for representing the entities used by a light board (cues, subs,
etc) in the :mod:`entities` module, as well as several built-in entities in its submodules. In
addition, it provides certain constants and classes for entity fields and field types in the
:mod:`fields` module.

The Entities Framework
=======================================

.. module:: entities
   :synopsis: The base classes of the entities framework.

The :mod:`entities` module defines two base classes, :class:`Entity` and :class:`DictEntity`.
Entities should inherit from one of them.

The Entity Interface
---------------------------------------

In order for an object to be an entity, it must provide the entity interface. This is defined by
the :class:`Entity` class and is described here:

.. class:: Entity

   All entities should inherit from this class, as it provides the :meth:`send` method:

   .. automethod:: send

   An entity must also define the key sequence needed to send it to :term:`EOL`. This can be done
   in one of two ways, defining :attr:`keystr` or overriding :meth:`_keys` (which is usually the
   preferred method).

   .. attribute:: keystr

      This attribute is only needed if using the default implementation of :meth:`_keys`,
      otherwise it may be ignored. It is set by the default constructor.

   .. method:: _keys

      If not overridden, the default implementation of :meth:`_keys` simply returns the object's
      :attr:`keystr` attribute. Otherwise, it should return a keystring suitable for sending
      with the :meth:`send` method.

Additional Functionality of the :class:`Entity` Class
-----------------------------------------------------------

In addition to the entity interface, the :class:`Entity` class provides nice string
representations of an entity object, as well as some other generic functionality.

.. autoclass:: Entity
   :members: from_keylist, from_nice

The :class:`DictEntity` Class
-----------------------------------------

The :class:`DictEntity` class inherits from :class:`Entity` and provides the entity interface,
as well as a dictionary interface to its fields and a :meth:`save` method that uses :mod:`pickle`
to persist data. In order to use it, it must be subclasses and certain attributes must be
provided.

.. class:: DictEntity

   The :class:`DictEntity` class provides convenient field validation and a useful implementation
   of :meth:`~Entity._keys`, as long as all fields are constants from the :mod:`fields` module.
   It also provides a nice string representation to subclasses and a :meth:`save` method.

   The default constructor is inherited from `dict`, which may be fine for simpler entities, or
   it may be overridden to provide default field values or require arguments.

   In order to use :class:`DictEntity`, these two attributes must be defined:

   .. attribute:: _fields

      This should be a sequence of field type constants from the :mod:`fields` module.

   .. attribute:: _keyformat

      This should be a :func:`keys.parse_str`\ -suitable string defining how the entity should be
      sent to :term:`EOL`. It may contain field names in all caps enclosed in `"{"` and `"}"`, as
      long as those fields names are field constants from the :mod:`fields` module. If they are
      not, they must be included as `"{e[FIELD_NAME]}"` instead.

   Here is an example of both :attr:`_fields` and :attr:`_keyformat`, taken from the
   :class:`~entities.cues.SubroutineStep` class (The :mod:`fields` module has been imported using
   ``from fields import *``):

   .. literalinclude:: /../entities/cues.py
	 :start-after: class SubroutineStep(
	 :end-before: def __init__(

   The :class:`DictEntity` class provides three ways to access and set fields. First, traditional
   dictionary access is supported::

     >>> my_entity = SomeDictEntity()
     >>> my_entity[fields.FIELD] = 5
     >>> my_entity[fields.FIELD]
     5
     >>> my_entity["FIELD"]
     5

   Fields may also be accessed using the dot operator::

     >>> my_entity.FIELD = 1
     >>> my_entity.FIELD
     1

   :class:`DictEntity` will even accept mixed-case field names with the dot operator::

     >>> my_entity.Field = 3
     >>> my_entity.field
     3

   When the dot operator is used, if the requested field is not present in :attr:`_fields`,
   it will simply try to get or set the attribute normally. However, when using dictionary
   access syntax, a `KeyError` will be raised if the field is not there::

     >>> my_entity.Invalid_Field
     Traceback (most recent call last):
     ...
     AttributeError: 'SomeDictEntity' object has no attribute 'Invalid_Field'
     >>> my_entity["INVALID_FIELD"]
     Traceback (most recent call last):
     ...
     KeyError: 'SomeDictEntity does not have a INVALID_FIELD field!'

   Additionally, :func:`fields.validateField` is used on all attempts to set field values. If it
   returns `False`, a `TypeError` is thrown.

   When certain fields are requested, they are returned in a special format suitable for
   :meth:`~Entity.send`. Labels are returned preceded by the keycode for F6 to clear an existing
   label and spaces are replaced with the special "space" keycode. A Level field is returned as
   `"Full"` if it is set to 100, otherwise it is returned as a zero-padded (if neccesary) string.

   Additionally, if an entity has a `TYPE` field, it may define the :attr:`_type` attribute.

   .. attribute:: _type

      This should be a string. If set, when the `TYPE` field is requested, this will be returned
      instead.

   :class:`DictEntity` provides a method for pickling and saving entity data in a python-only
   binary format. To restore this saved data, use :func:`pickle.load` from the standard libary.
   Alternatively, an entity can be saved in a nice human readable format, but note that said
   format is not readable back to a :class:`DictEntity` at this point, though it may be used
   with :func:`keys.parse_str` or :meth:`Entity.from_nice`.

   .. automethod:: save


Entity Fields – The :mod:`fields` Module
==============================================

.. automodule:: fields
   :synopsis: Provides field type constants and :term:`complex field` classes.

The :mod:`fields` module serves three purposes: it provides constants defining field types,
which are used heavily by classes like :class:`DictEntity`; it provides the :func:`validateField`
function; and it provides classes for some more :term:`complex field` types, such as :class:`Levels`.

.. Note:: A lot of the :mod:`fields` module's contents are badly implemented, and will likely
	  change at a later time to be more extensible.

Field Type Constants
----------------------------------

The :mod:`fields` module defines the following field types::

  CUE
  LABEL
  TYPE
  UPTIME
  DOWNTIME
  UPWAIT
  DOWNWAIT
  DWELL
  LINK
  FOLLOW
  RATE
  LEVEL
  LEVELS
  STEP
  STEPS
  STYLE
  DWEKK
  TIME
  LOW/LOWLEVEL
  HIGH/HIGHLEVEL
  CHANNELS

The :func:`validateField` Function – Field Validation
-------------------------------------------------------

This function is also used by :class:`DictEntity` to attempt to ensure the validity of field
values. At the moment it validates a very limited set of fields.

.. autofunction:: validateField

Complex Field Types
-------------------------------------------------------

The :mod:`fields` module provides three base classes which other :term:`complex field`\ s should
inherit from.

.. Note:: A :term:`complex field` is defined as an entity field which cannot be represented
	  using a string or integer or has multiple sub-fields.

Complex fields must define `__str__` such that when they are inserted into a keystring such as
:attr:`DictEntity._keyformat' they provide the right representation to send to :term:`EOL`.

.. class:: Field()

   The base field class. It does not actually do anything, and is only useful for type checking.

.. class:: DictField(**kwargs)

   Much like :class:`Field`, it does nothing other than inherit from both :class:`Field` and
   `dict`.

.. autoclass:: List

   This class implements validation as well as a recursive `__str__` function, on top of the
   standard `list` interface.

   When initialized, the first argument, `type_`, should be the type of the objects that the
   :class:`List` should contain. When objects are added or set, their type is checked against
   it. Additional arguments are passed to the `list` constructor and will therefore be included
   in the list.

   Converting a :class:`List` to a string is done by converting each element to a string and
   joining the results with newlines.

The :mod:`fields` module also provides a :class:`Levels` :term:`complex field` class for
representing a set of levels, such as in a cue or submaster.

.. class:: Levels

   The :class:`Levels` class inherits from class:`DictField` and therefore uses the dictionary
   interface for settings level values. Unfortunately, it is hardwired for a 192 channel console,
   which will probably change at somepoint.

   Unlike a :class:`~entities.DictEntity`, getting levels still returns an integer, and it is
   only when the object is converted to a string that level values are normalized for :term:`EOL`.

   :class:`Levels` may also be used as a base class for special level collections. If a class
   inherits from it, it may use all of the same interfaces and just provide a different
   :attr:`_channel_format` attribute to cause the object to be converted to a string in a
   different way.

   .. attribute:: _channel_format

      This should be a string much like :attr:`~entities.DictEntity._keyformat`, except with
      two built in keys, `"{chan}"` and `"{level}"`. When the object is converted to a string,
      :attr:`_channel_format` is used with each set level, where `"{chan}"` is replaced with the
      channel number and `"{level}"` is replaced with its level.

      The default value is ``"Channel {chan} at {level}"``, but it can be set to anything.
