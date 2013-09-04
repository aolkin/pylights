.. Documentation of built-in entities

.. |type| replace:: :const:`~pylights.entities.fields.TYPE`

Built-In Entities
*********************************************

PyLights provides several common entities in the :mod:`pylights.entities` module.

.. Note:: Unless otherwise specified, all documented modules on this page are submodules of the
	  :mod:`pylights.entities` module.

All entities described on this page use :ref:`the-entity-interface`. As such, they all inherit
send, which is used to send the entity to :term:`EOL`.

.. automethod:: pylights.entities.Entity.send
   :noindex:

Cues
=============================================

.. module:: pylights.entities.cues
   :synopsis: Provides cue entities.

The :mod:`~pylights.entities.cues` module provides three cue classes and three classes used by some of the
cue classes, as well as some useful constants for cue types.

The :class:`Cue` Class – A Basic Cue
---------------------------------------------

Of the five types of cues (Crossfade, Allfade, Blocking, Effect, and Subroutine), the first three
should all be created using the :class:`Cue` class. Those three cue types should then be
differentiated by the cue |type| field.

.. autoclass:: Cue

   You must provide a cue's number on instantiation, though it may be changed after.

   This class is setup so that if a field is unspecified, it should use the console's default.

   A basic cue has the following fields:

   .. literalinclude:: /../pylights/entities/cues.py
      :start-after: class Cue(
      :end-before: _keyformat = 

.. _cue-type-constants:

Cue Type Constants
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :mod:`~pylights.entities.cues` module also provides three constants (with abbreviated aliases) for
different cue types.

.. data:: XF
.. data:: CROSSFADE

   The |type| of a crossfade cue.

.. data:: AF
.. data:: ALLFADE

   The |type| of an allfade cue.

.. data:: BF
.. data:: BLOCKING

   The |type| of a blocking cue.

Subroutines – The :class:`SubroutineCue` and :class:`SubroutineStep` Classes
-----------------------------------------------------------------------------

A Subroutine Cue should be not be created using the :class:`Cue` class, but rather the
:class:`SubroutineCue` class.

.. Note:: :class:`SubroutineCue` does not inherit from :class:`Cue`.

.. autoclass:: SubroutineCue

   A :class:`SubroutineCue` functions much like an :class:`Cue`, except with many fewer fields.
   Additionally, its |type| will always be forced to `4`.

   .. literalinclude:: /../pylights/entities/cues.py
      :start-after: class SubroutineCue(
      :end-before: _type = 

   The :const:`~pylights.entities.fields.STEPS` field should never be set directly, instead, it is a
   :class:`pylights.entities.fields.List` to which :class:`SubroutineStep` objects should be added.

.. autoclass:: SubroutineStep

   A :class:`SubroutineStep` has the following fields:

   .. literalinclude:: /../pylights/entities/cues.py
      :start-after: class SubroutineStep(
      :end-before: _keyformat = 

   Once again, the :ref:`cue-type-constants` may be used for the |type| field.

Effect Cues – The :class:`EffectCue` and :class:`EffectStep` Classes
------------------------------------------------------------------------

Effect Cues should be created using the :class:`EffectCue` class.

.. autoclass:: EffectCue

   An :class:`EffectCue` has most of the fields of a :class:`Cue`, but in most ways it functions
   more like a :class:`SubroutineCue`. Its |type| will be forced to `3`.

   .. literalinclude:: /../pylights/entities/cues.py
      :start-after: class EffectCue(
      :end-before: _type = 

   The :const:`~pylights.entities.fields.STEPS` field is a :class:`pylights.entities.fields.List` to which :class:`EffectStep`
   objects should be added.

.. autoclass:: EffectStep

   An :class:`EffectStep` has the following fields:

   .. literalinclude:: /../pylights/entities/cues.py
      :start-after: class EffectStep(
      :end-before: _keyformat = 

   Its :const:`~pylights.entities.fields.CHANNELS` field is an :class:`EffectChannels` object that inherits from
   and behaves as a :class:`pylights.entities.fields.Levels` object. After object creation, all changes should be
   made using that interface.

.. class:: EffectChannels

   This class does little other than inherit from :class:`pylights.entities.fields.Levels` and redefine
   :attr:`~pylights.entities.fields.Levels._channel_format`.
