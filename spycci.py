import datetime
from itertools import imap

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class Movement(dict):
    '''describe a money movement'''
    def __init__(self, d={}):
        #TODO: use kwargs
        for key, value in d.items():
            self[key] = value

    def __str__(self):
        return '<Movement: %d>' % self.money
    
    def update(self, *args, **kwargs):
        for k,v in dict(*args, **kwargs).iteritems():
            self[k] = v

    #setters are here; who knows why this is needed...
    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError(key)
    def __getitem__(self, key):
        if key == 'tags':
            return dict.__getitem__(self, 'tags') if 'tags' in self else set()
        elif key == 'other':
            return dict.__getitem__(self, 'other') if 'other' in self else ''
        elif key == 'date':
            return dict.__getitem__(self, 'date') if 'date' in self else datetime.date(1970,1,1)
        elif key == 'money':
            return dict.__getitem__(self, 'money') if 'money' in self else 0

        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return ''
    def __setitem__(self, key, value):
        if key == 'date':
            if value:
                dict.__setitem__(self, key, datetime.date(
                    *[int(x) for x in value.split('-')]))
        elif key == 'tags':
            dict.__setitem__(self, key, set(value))
        else:
            dict.__setitem__(self, key, value)

class Balance(list):
    '''a list of Movement, with nice methods'''
    def __init__(self, movements=[]):
        self.extend(movements)

    def filter(self, function):
        return Balance([m for m in self if function(m)])

    def filter_period(self, start=0, end=None):
        '''Get movements between start and end'''
        if end is None:
            end = datetime.date.today()
        return self.filter(lambda m: start < m['date'] < end)
    def filter_tags(self, tags):
        '''this filter for ANY tag in tags (they are ORed)'''
        return self.filter(lambda m: not m['tags'].isdisjoint(tags))
    def filter_other(self, other):
        return self.filter(lambda m: m['other'] == other)

    def get_others(self):
        return frozenset((x['other'] for x in self if x['other']))
    def total(self):
        return sum((m['money'] for m in self))

    def __str__(self):
        return '<Balance: #%d>' % len(self)
    def __getitem__(self, item_or_slice):
        if type(item_or_slice) is int:
            return list.__getitem__(self, item_or_slice)
        elif type(item_or_slice) is slice:
            return Balance(list.__getitem__(self, item_or_slice))
        else:
            raise ValueError('<%s> is not a valid type for indexing a Balance'
                    % type(item_or_slice))
    def __getslice__(self, start, end):
# we need this because list implements it; so we have to override, even if
# the logic is already contained in __getitem__ and __getslice__ is deprecated
        return self.__getitem__(slice(start, end, 1))

def get_balance(filename):
    '''read a yaml file and get a Balance'''
    with open(filename, 'r') as f:
        data = yaml.load(f, Loader=Loader)
        b = Balance(imap(Movement, (m for m in data)))
        return b

#TODO: a cli that is based on ipython

if __name__ == '__main__':
    import sys
    b = get_balance('asd.yaml')
    print b, [str(m) for m in b]
    print [(m.good, m.other) for m in b if m.money == 0]
    sys.exit(0)
############# convert to unit tests
    b = Balance()
    b.append(Movement(-10, tags={'foo', 'baz'}))
    b.append(Movement(+5, date=time.time() - 60*60*24,
        tags={'asd', 'foo'}))
    b2 = b.filter_period(time.time() - 3600, time.time() - 60)
    print b2, [str(m) for m in b2]
    b2 = b.filter_period(time.time() - 3600, time.time() + 60)
    print b2, [str(m) for m in b2]
    b2 = b.filter_period()
    print 'until now', b2, [str(m) for m in b2]
    b2 = b.filter_tags({'asd'})
    print 'asd', b2, [str(m) for m in b2]
    b2 = b.filter_tags({'foo'})
    print 'foo', b2, [str(m) for m in b2]
    b2 = b.filter_tags({'asd', 'baz'})
    print 'asd baz', b2, [str(m) for m in b2]

# vim: set ts=4 sw=4 expandtab:
