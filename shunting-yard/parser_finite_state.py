from typing import Any, Tuple, List
from collections import namedtuple
import re

StateRet = namedtuple('StateRet', ['next_state', 'done', 'increment'])
MATH_SYMBOLS = ('+', '-', '*', '**', '/',  '^', '//', '%', '(', ')')


def word_state(char: str, stack: List[str]) -> StateRet:
    """
    Returns:
            Tuple of: next state, if state is complete, if read next char, if append char
    """

    if re.match("([a-z]|[A-Z])", char):
        stack.append(char)
        return StateRet(word_state, False, True)

    else:
        return StateRet(start_state, True, False)


def num_pre_dot_state(char: str, stack: List[str]) -> StateRet:
    """ Returns:
            Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char.isdigit():
        stack.append(char)
        return StateRet(num_pre_dot_state, False, True)

    elif char == '.':
        stack.append(char)
        return StateRet(num_post_dot_state, False, True)

    elif char in MATH_SYMBOLS:
        return StateRet(sym_state, True, False)

    else:
        raise Exception("Missing operator between number and letter: {}{}".format(''.join(stack), char))


def num_post_dot_state(char: str, stack: List[str]) -> StateRet:
    """ Returns:
            Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char.isdigit():
        stack.append(char)
        return StateRet(num_post_dot_state, False, True)

    elif char in MATH_SYMBOLS:
        return StateRet(sym_state, True, False)

    elif char == '.':
        raise Exception("Too many dots: {}.". format(''.join(stack)))

    else:
        raise Exception("Missing operator between number and letter: {}{}".format(''.join(stack), char))


def sym_state(char: str, stack: List[str]) -> StateRet:
    """ Returns:
            Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char == '+':
        stack.append(char)
        return StateRet(plus_state, False, True)

    if char == '-':
        stack.append(char)
        return StateRet(minus_state, False, True)


    #if char != '*':
    #    return StateRet(start_state, True, True, True)

    #if char == '*':
    #    return StateRet(second_mul_state, False , True, True)

    #if char == ''


#def _pop(char: str, stack: List[str]) -> StateRet:
#    stack.pop()


def plus_state(char: str, stack: List[str]) -> StateRet:

    if char == '+':
        return StateRet(plus_state, False, True)

    elif char == '-':
        stack.pop()
        stack.append(char)
        return StateRet(minus_state, False, False)

    elif char in ['*', '/', '^', '%']:
        raise Exception("Illegal combination of operators: +{}".format(char))

    else:
        return StateRet(start_state, True, False)


def minus_state(char: str, stack: List[str]) -> StateRet:

    if char == '-':
        stack.pop()
        stack.append('+')
        return StateRet(plus_state, False, True)

    elif char == '+':
        return StateRet(minus_state, False, True)

    elif char in ['*', '/', '^', '%']:
        raise Exception("Illegal combination of operators: +{}".format(char))

    else:
        return StateRet(start_state, True, False)



def non_additive_state(char: str, stack: List[str]) -> StateRet:
    pass


def second_mul_state(char: str, stack: List[str]) -> StateRet:
    """ Returns:
                Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char == '*':
        stack.append(char)
        return StateRet(start_state, True, True)

    else:
        return StateRet(start_state, True, False)


def start_state(char: str, stack: List[str]) -> StateRet:
    """ Returns:
            Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char.isdigit():
        stack.append(char)
        return StateRet(num_pre_dot_state, False, True)

    elif char == '.':
        stack.append(char)
        return StateRet(num_post_dot_state, False, True)

    elif char in MATH_SYMBOLS:
        return StateRet(sym_state, False, False)

    elif re.match('([a-z]|[A-Z])', char):
        stack.append(char)
        return StateRet(word_state, False, True)

    else:
        raise Exception('Illegal character:{}'.format(char))


if __name__ == '__main__':

    'next_state', 'done', 'increment', 'append'

    input_string = "3+++---1"



    stack = []
    output_list = []

    idx = 0
    state = start_state

    while True:
        char = input_string[idx]

        return_state = state(char, stack)

        if return_state.increment:
            idx +=1

        #if return_state.append:
        #    stack.append(char)

        if return_state.done or idx == len(input_string):
            output_list.append(''.join(stack))
            stack = []
            if idx == len(input_string):
                break

        state = return_state.next_state

    print(output_list)