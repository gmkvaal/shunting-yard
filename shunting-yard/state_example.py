
from typing import Any, Tuple, List

from collections import namedtuple

StateRet = namedtuple('StateRet', ['next_state', 'done', 'increment'])

def start(c: str, stack: List[str]) -> StateRet:
    """
    Returns:
        Tuple of next state, if the stack is ready, if the read head should increment
    """
    if c in {'+', '-'}:
        stack.append(c)
        return StateRet(start, True, True)
    elif c in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
        stack.append(c)
        return StateRet(num_state, False, True)
    else:
        raise ValueError()

def num_state(c: str, stack: List[str]) -> StateRet:
    if c in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
        stack.append(c)
        return StateRet(num_state, False, True)
    elif c in {'+', '-'}:
        return StateRet(start, True, False)
    else:
        raise ValueError()


if __name__ == '__main__':
    inp = input('>>> ')

    inp_ptr = 0
    state = start
    stack = []

    while True:
        c = inp[inp_ptr]

        state_return = state(c, stack)
        state = state_return.next_state

        if state_return.increment:
            inp_ptr += 1

        if state_return.done or len(inp) == inp_ptr:
            print(''.join(stack))
            stack = []
            if len(inp) == inp_ptr:
                break
