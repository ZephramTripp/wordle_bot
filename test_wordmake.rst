test_wordmake
=============

Good for testing! Probably should be restructured to be more object oriented!

.. automodule:: test_wordmake
    :members:

Tests
~~~~~

.. testsetup:: *
    import wordmake

.. doctest::

    >>> wordmake(['a', 'b', 'c', 'd'], 2)
    ['aa', 'ab', 'ac', 'ad', 'ba', 'bb', 'bc', 'bd', 'ca', 'cb', 'cc', 'cd', 'da', 'db', 'dc', 'dd']

Table of starting words
~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table:: All Starting Words
    :file: results.txt
    :widths: 30, 40, 30
    :header: Words,Avg Guesses,Failures
    :header-rows: 0
