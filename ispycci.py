import sys

from IPython import embed
import spycci
from prettytable import PrettyTable

filename = sys.argv[1]
b = spycci.get_balance(filename)

def show(mov_or_bal=b, verbose=False):
    def _show_mov(mov):
        if verbose:
            print mov
        else:
            print {key:str(value) for key,value in mov.items() if value}
    if type(mov_or_bal) is spycci.Movement:
        _show_mov(mov_or_bal)
    else: #assume Balance
        for m in mov_or_bal:
            _show_mov(m)
#    return mov_or_bal

def table(bal=b, **kwargs):
    '''first argument (optional) is the balance;
    then kw args for printing table:
    - sortby = name of column
    - reversesort = false/true
    - fields = list of columns
    - start = row number (included)
    - end = row number (not included)
    '''
    headers = set()
    for m in bal:
        headers.update({k for k in m.keys()})
    headers = tuple(headers)
    tab = PrettyTable(headers)
    for m in bal:
        fields = []
        for h in headers:
            fields.append(m[h])
        tab.add_row(fields)
    args = { 'sortby': 'date' } if 'date' in headers else {}
    args.update(kwargs)
    print tab.get_string(**args)



embed()
