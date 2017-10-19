from typing import Any, Tuple, List
from collections import namedtuple
import re

StateRet = namedtuple('StateRet', ['next_state', 'done', 'increment', 'append'])
MATH_SYMBOLS = ('+', '-', '*', '/', '**', '(', ')')


def word_state(char: str, stack: List[str]) -> StateRet:
    """
    Returns:
            Tuple of: next state, if state is complete, if read next char, if append char
    """

    if re.match("([a-z]|[A-Z])", char):
        return StateRet(word_state, False, True, True)

    else:
        return StateRet(start_state, True, False, False)


def num_pre_dot_state(char: str, stack: List[str]) -> StateRet:
    """ Returns:
            Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char.isdigit():
        return StateRet(num_pre_dot_state, False, True, True)

    elif char == '.':
        return StateRet(num_post_dot_state, False, True, True)

    elif char in MATH_SYMBOLS:
        return StateRet(sym_state, False, False, False)

    else:
        raise Exception("Missing operator between number and letter: {}{}".format(''.join(stack), char))


def num_post_dot_state(char: str, stack: List[str]) -> StateRet:
    """ Returns:
            Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char.isdigit():
        return StateRet(num_post_dot_state, False, True, True)

    elif char == '.':
        raise Exception("Too many dots: {}.". format(''.join(stack)))

    else:
        return StateRet(start_state, True, False, False)


def sym_state(char: str, stack: List[str]) -> StateRet:
    """ Returns:
            Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char == '*':
        return StateRet(start_state, True, True, True)

    else:
        return StateRet(start_state, True , False, False)


def start_state(char: str, stack: List[str]) -> StateRet:
    """ Returns:
            Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char.isdigit():
        return StateRet(num_pre_dot_state, False, True, True)

    elif char == '.':
        return StateRet(num_post_dot_state, False, True, True)

    elif char in MATH_SYMBOLS:
        return StateRet(sym_state, False, True, True)

    elif re.match('([a-z]|[A-Z])', char):
        return StateRet(word_state, False, True, True)

    else:
        raise Exception('Illegal character:{}'.format(char))


if __name__ == '__main__':

    'next_state', 'done', 'increment', 'append'

    input_string = "3+(3.14)"



    stack = []
    output_list = []

    idx = 0
    state = start_state

    while True:
        char = input_string[idx]

        return_state = state(char, stack)

        if return_state.increment:
            idx +=1

        if return_state.append:
            stack.append(char)

        if return_state.done or idx == len(input_string):
            output_list.append(''.join(stack))
            stack = []
            if idx == len(input_string):
                break

        state = return_state.next_state

    print(output_list)