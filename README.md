spycci
======

This is basically a non-manager for your money/things.
It also features a non-interface for it.
You were waiting for it, admit it

Concepts
--------

Reality is too difficult to be modelled with a clean, relational structure;
let's go wild, flat; let's abandon any order.

### What's a "balance"?

it is a list of movements

### What's a movement?

It is a flow of money/things between you and one other
subject.

### What properties has a movement

Whatever you want. You can add any metadata you want and it will be preserved.

However, some attributes are special. They are:
- date, which must be wrote as a 'YYYY-MM-DD' string
- money, it will default to 0 if not present
- tags, it will default to empty set()
- other, which is a string describing the other subject
- good: it's a "thing" that you received/borrowed. If it flows from $other to
  you, you will write good: something
  In the other case, you'll write good: -something

Balance file
------------

It's a YAML file.
YAML is quite nice, readable, and supports different styles, comments... lots
of nice things.

Here's an example:

    - { good: the art of computer programming, other: guy1, date: '2012-01-20' }
    - { good: -laptop, other: guy1}
    - { money: -132.5, other: guy2, reason: 'some expenses about FOO', tags: ['project_foo'] }
    - { money: 100, other: guy2, reason: giving back part of the FOO money, date: '2012-07-27', tags: ['project_foo'] }

(that is, I borrowed a laptop to guy1, who gived me "the art of computer
programming"; also, I gave 132.5 € to guy2, who gave me back only 100)

Interface
---------

It is an ipython instance with some useful functions already loaded in. Your
data will be loaded automatically inside variable "b".

Writing `table()`, you'll have a nice display.
With `b.total()`, you'll get (guess what?) the total for your movements
To filter the balance, just use the `filter*` methods:
`b.filter_other('myfriend')`, will create a new balance with just the required
movements.

    table(b.filter_other('myfriend'))

filtering is chainable!

    b.filter_other('myfriend').filter_tag(['mytag'])

You can get all the people you have movements with, using

	b.get_others()

And you can write your own complex filter using

	b.filter(func_or_lambda)

**NOTE**: there's no interface to add/edit your balance; use $EDITOR

vim: set tw=79 ft=markdown:
