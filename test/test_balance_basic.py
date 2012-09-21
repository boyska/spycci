from spycci import Movement, Balance

from nose.tools import assert_is, assert_equal

movements = map(Movement, [
    {'money': 100, 'other': 'X Guy'},
    {'good': 'bookA', 'other': 'Y Guy'},
    {'money': -20, 'other': 'Y Guy'}
    ])
std_bal = Balance(movements)

def test_create_basic():
    assert_is(type(std_bal), Balance)
    assert_equal(len(std_bal), len(movements))
    assert len(std_bal) == 3
    assert_equal(std_bal[0]['money'], 100)
    assert_equal(std_bal[1]['money'], 0)
    assert_equal(std_bal[2]['money'], -20)

def test_get_others():
    ot = std_bal.get_others()
    assert_equal(len(ot), 2)
    assert_equal(ot, set(('X Guy', 'Y Guy')))
    assert_equal(ot, set(('Y Guy', 'X Guy')))

def test_total():
    assert std_bal.total() == 80
    assert std_bal[:1].total() == 100
    assert std_bal[-1:].total() == -20



# vim: set ts=4 sw=4 expandtab:
