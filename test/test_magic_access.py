from spycci import Movement, Balance

movements = map(Movement, [
    {'money': 100, 'other': 'X Guy'},
    {'good': 'bookA', 'other': 'Y Guy'},
    {'money': -20, 'other': 'Y Guy'}
    ])
std_bal = Balance(movements)

def test_access():
    '''access to Movement is available both dict- and class-style'''
    assert std_bal[0]['money'] == 100
    assert std_bal[0].money == 100
    assert std_bal[1]['money'] == 0
    assert std_bal[1].money == 0

def test_slice():
    '''Balance supports slicing'''
    sl = std_bal[0:1]
    assert type(sl) is Balance
    assert len(sl) == 1
    assert sl[0]['money'] == 100
    sl = std_bal[-1:]
    assert type(sl) is Balance
    assert len(sl) == 1
    assert sl[0]['money'] == -20
    sl = std_bal[0:3:2]
    assert type(sl) is Balance
    assert len(sl) == 2
    assert sl[0]['money'] == 100
    assert sl[1]['money'] == -20
