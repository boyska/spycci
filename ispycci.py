import sys

from IPython import embed
import spycci

filename = sys.argv[1]
b = spycci.get_balance(filename)

def show(mov_or_bal=b, verbose=False):
    def _show_mov(mov):
        if verbose:
            print mov.__dict__
        else:
            print {key:value for key,value in mov.__dict__.items() if value}
    if type(mov_or_bal) is spycci.Movement:
        _show_mov(mov_or_bal)
    else: #assume Balance
        for m in mov_or_bal:
            _show_mov(m)
    return mov_or_bal

embed()
