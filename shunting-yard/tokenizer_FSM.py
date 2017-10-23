from typing import List
from settings import MATH_SYMBOLS
from collections import namedtuple
from token_classifier import append_token
import re


"""
Finite State Machine algorithm for parsing mathematical expression.

Supports operators in MATH_SYMBOLS tuple (e.g. not binaries)
"""

StateRet = namedtuple('StateRet', ['next_state', 'done', 'increment'])


def start_state(char: str, stack: List[str]) -> StateRet:
    """  Start state. Directs  to respective states.

    Returns:
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
        raise Exception('Illegal character or '
                        'illegal character placement:{}'.format(char))


def word_state(char: str, stack: List[str]) -> StateRet:
    """ Appends word-characters to stack. Dumps when reaching another type.

    Returns:
            Tuple of: next state, if state is complete, if read next char, if append char.
    """

    if re.match("([a-z]|[A-Z])", char):
        stack.append(char)
        return StateRet(word_state, False, True)

    elif char == ',':
        return StateRet(comma_state, True, False)

    else:
        return StateRet(start_state, True, False)


def num_pre_dot_state(char: str, stack: List[str]) -> StateRet:
    """ Appends digits to stack. If reaching dot, switching to num_post_dot_state.
    Dumps when reaching math symbol / operator. Error if reaching word character,
    e.g., 2b is not accepted.

    Returns:
            Tuple of: next state, if state is complete, if read next char, if append char.
    """

    if char.isdigit():
        stack.append(char)
        return StateRet(num_pre_dot_state, False, True)

    elif char == '.':
        stack.append(char)
        return StateRet(num_post_dot_state, False, True)

    elif char == ',':
        return StateRet(comma_state, True, False)

    elif char in MATH_SYMBOLS:
        return StateRet(sym_state, True, False)

    else:
        raise Exception("Missing operator between number and letter: "
                        "{}{}".format(''.join(stack), char))


def num_post_dot_state(char: str, stack: List[str]) -> StateRet:
    """ Only called after num_pre_dot_state. Appends digits to stack.
    Dumps when reaching symbol / operator. Error if reaching dot or word character,
    e.g., 2b or 1.1.1 are not accepted

    Returns:
            Tuple of: next state, if state is complete, if read next char, if append char.
    """

    if char.isdigit():
        stack.append(char)
        return StateRet(num_post_dot_state, False, True)

    elif char in MATH_SYMBOLS:
        return StateRet(sym_state, True, False)

    elif char == ',':
        return StateRet(comma_state, True, False)

    elif char == '.':
        raise Exception("Too many dots: {}.". format(''.join(stack)))

    else:
        raise Exception("Missing operator between number and letter: "
                        "{}{}".format(''.join(stack), char))


def sym_state(char: str, stack: List[str]) -> StateRet:
    """ Appends symbols / operators. If char is * or /, respective states are called
    in case token is ** or //.

    Returns:
            Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char in ['+', '-', '%', '(', ')']:
        stack.append(char)
        return StateRet(start_state, True, True)

    if char == '*':
        stack.append(char)
        return StateRet(mul_state, False, True)

    if char == '/':
        stack.append(char)
        return StateRet(div_state, False, True)


def mul_state(char: str, stack: List[str]) -> StateRet:
    """ Only called if previous char was *. Dumps ** if (current) char is *,
    else returns start_state

    Returns:
        Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char == '*':
        stack.append(char)
        return StateRet(start_state, True, True)

    else:
        return StateRet(start_state, True, False)


def div_state(char: str, stack: List[str]) -> StateRet:
    """ Only called if previous char was *. Dumps ** if (current) char is *,
    else returns start_state

    Returns:
        Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char == '/':
        stack.append(char)
        return StateRet(start_state, True, True)

    else:
        return StateRet(start_state, True, False)


def comma_state(char: str, stack: List[str]) -> StateRet:
    """Only called when char is comma"""

    stack.append(char)
    return StateRet(start_state, True, True)


def tokenizer(input_string):
    """Splits an input string into list of tokens by
    a finite state machine algorithm"""

    stack = []
    output_list = []
    idx = 0
    state = start_state

    while True:
        char = input_string[idx]
        return_state = state(char, stack)


        if return_state.increment:
            idx += 1

        if return_state.done or idx == len(input_string):
            print(state.__name__, ''.join(stack))

            output_list.append(''.join(stack))
            stack = []
            if idx == len(input_string):
                break

        state = return_state.next_state

    return output_list



if __name__ == '__main__':

    input_string = "1**-max(4,2)*cos(3)"

    print(tokenizer(input_string))