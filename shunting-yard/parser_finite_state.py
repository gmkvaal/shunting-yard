from typing import Any, Tuple, List
from collections import namedtuple
import re

StateRet = namedtuple('StateRet', ['next_state', 'done', 'increment', 'append'])
MATH_SYMBOLS = ('+', '-', '*', '/', '**', '(', ')')


def word_state(char: str, stack: List[str]) -> StateRet:
    """ Returns:
            Tuple of next state, if state is complete, if read next char
    """

    if re.match("([a-z]|[A-Z])", char):
        return StateRet(word_state, False, True, True)

    else:
        return StateRet(start_state, True, True, False)


def num_state(char: str, stack: List[str]) -> StateRet:
    """ Returns:
            Tuple of next state, if state is complete, if read next char
    """

    if char.isdigit() or char == '.':
        return StateRet(num_state, False, True, True)

    else:
        return StateRet(start_state, True, True, False)


def sym_state(char: str, stack: List[str]) -> StateRet:
    """ Returns:
            Tuple of next state, if state is complete, if read next char
    """

    if char == '*'
        return StateRet(start_state, False, True, True)

    else:
        return StateRet(start_state, True , True, False)


def start_state(char: str, stack: List[str]) -> StateRet:
    """
    :param char: pointet character in input string
    :param stack: output
    :return: Tuple of next state, if state ready, if head should increment
    """

    if char.isdigit() or char == '.':
        return StateRet(num_state, False, True, True)

    elif char in MATH_SYMBOLS:
        return StateRet(sym_state, False, False, True)

    elif re.match("([a-z]|[A-Z])", char):
        return StateRet(word_state, False, True, True)

    else:
        raise Exception('Illegal character:{}'.format(char))


if __name__ == '__main__':

    'next_state', 'done', 'increment', 'append'

    input_string = "3.14+1"
    stack = []

    idx = 0

    state = start_state

    while True:
        char = input_string[idx]

        print(char)

        return_state = state(char, stack)
        #print(return_state)
        return_state.next_state(char, stack)

        if return_state.increment:
            idx +=1

        if return_state.append:
            stack.append(char)

        if return_state.done or idx == len(input_string):
            print(''.join(stack))
            stack = []
            if idx == len(input_string):
                break
