from spycci import Movement

def test_create_movement():
    m = Movement({})
    m = Movement({'money': 100, 'other': 'X Guy'})

def test_movement_special_fields():
    m = Movement({'money': 100, 'other': 'X Guy'})
    assert m['money'] == 100.0
    assert m['tags'] == set()
    assert m['good'] == ''
    assert m['other'] == 'X Guy'
    m = Movement({'foofield': 'foozavalue'})
    assert m['money'] == 0
    assert m['tags'] == set()
    assert m['good'] == ''
    assert m['other'] == ''

def test_movement_custom_fields():
    m = Movement({'foofield': 'foozavalue'})
    assert m['foofield'] == 'foozavalue'
    assert m['nonexist'] == ''

# vim: set ts=4 sw=4 expandtab:
