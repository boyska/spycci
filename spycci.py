import datetime
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

    #boring defaults
    @property
    def money(self):
        '''Money amount'''
        return self['money'] if 'money' in self else 0
    @property
    def tags(self):
        if 'tags' not in self:
            self.tags = set()
        return self['tags']
    @property
    def other(self):
        return self['other'] if 'other' in self else ''
    @property
    def date(self):
        return self['date'] if 'date' in self else datetime.date(1970,1,1)

    def __str__(self):
        return '<Movement: %d>' % self.money
    
    def update(self, *args, **kwargs):
        for k,v in dict(*args, **kwargs).iteritems():
            self[k] = v

    #setters are here; who knows why this is needed...
    def __setitem__(self, key, value):
        if key == 'date':
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
        return self.filter(lambda m: start < m.date < end)
    def filter_tags(self, tags):
        '''this filter for ANY tag in tags (they are ORed)'''
        return self.filter(lambda m: not m.tags.isdisjoint(tags))

    def get_others(self):
        return frozenset((x.other for x in self if x.other))
    def total(self):
        return sum((m.money for m in self))

    def __str__(self):
        return '<Balance: #%d>' % len(self)

def get_balance(filename):
    '''read a yaml file and get a Balance'''
    b = Balance()
    with open(filename, 'r') as f:
        data = yaml.load(f, Loader=Loader)
        for m in data:
            movement = Movement(m)
            b.append(movement)

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