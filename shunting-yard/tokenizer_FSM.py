from typing import List
from collections import namedtuple
from settings import MATH_SYMBOLS
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
            Tuple of: next state, if state is complete (never), if read next char, if append char
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

    if char in '(':
        stack.append(char)
        return StateRet(left_parenthesis_state, True, True)

    if char in ')':
        stack.append(char)
        return StateRet(right_parenthesis_state, True, True)

    if char == '%':
        stack.append(char)
        return StateRet(operator_state, True, True)

    if char == '-':
        stack.append(char)
        return StateRet(minus_state, False, True)

    if char == '+':
        stack.append(char)
        return StateRet(plus_state, False, True)

    if char == '*':
        stack.append(char)
        return StateRet(mul_state, False, True)

    if char == '/':
        stack.append(char)
        return StateRet(div_state, False, True)


def left_parenthesis_state(char: str, stack: List[str]) -> StateRet:

    if char in MATH_SYMBOLS and char not in ['+', '-']:
        raise Exception("Non addidive operator after left parenthsis: ({}.".format(char))

    if char == '+':
        return StateRet(plus_post_operator_state, True, False)

    if char == '-':
        return StateRet(minus_post_operator_state, True, False)

    else:
        return StateRet(start_state, False, False)


def right_parenthesis_state(char: str, stack: List[str]) -> StateRet:

    if re.match('[0-9]'):
        raise Exception("Missing operator between right parenthesis and number: "
                        "){}".format(char))

    if re.match("([a-z]|[A-Z])", char):
        raise Exception("Missing operator between right parenthesis and letter: "
                        "){}".format(char))

    else:
        return StateRet(start_state, False, False)


def operator_state(char: str, stack: List[str]) -> StateRet:

    if char in MATH_SYMBOLS and char not in ['(']:
        raise Exception('Operator after operator')

    else:
        return StateRet(start_state, False, False)


def plus_state(char: str, stack: List[str]) -> StateRet:

    if char == '+':
        return StateRet(plus_state, False, True)

    elif char == '-':
        stack.pop()
        stack.append(char)
        return StateRet(minus_state, False, True)

    elif char in ['*', '/', '^', '%']:
        raise Exception("Illegal combination of operators: +{}".format(char))

    else:
        return StateRet(start_state, True, False)


def minus_state(char: str, stack: List[str]) -> StateRet:

    if char == '-':
        stack.pop()
        return StateRet(start_state, False, True)

    elif char == '+':
        return StateRet(minus_state, False, True)

    elif char in ['*', '/', '^', '%']:
        raise Exception("Illegal combination of operators: {}"
                        "after additive operator".format(char))

    else:
        return StateRet(start_state, True, False)


def plus_post_operator_state(char: str, stack: List[str]) -> StateRet:

    if char == '+':
        return StateRet(plus_post_operator_state, False, True)

    elif char == '-':
        stack.pop()
        stack.append(char)
        return StateRet(minus_post_operator_state, False, False)

    elif char in ['*', '/', '^', '%']:
        raise Exception("Illegal combination of operators: +{}".format(char))

    else:
        return StateRet(start_state, False, False)


def minus_post_operator_state(char: str, stack: List[str]) -> StateRet:

    if char == '-':
        if len(stack) == 1:
            stack.pop()
        else:
            stack.append('-')
        return StateRet(minus_post_operator_state, False, True)

    elif char == '+':
        return StateRet(minus_post_operator_state, False, True)

    elif char in ['*', '/', '^', '%']:
        raise Exception("Illegal combination of operators: +{}".format(char))

    else:
        stack.append('1')
        return StateRet(artificial_mul_state, True, False)


def mul_state(char: str, stack: List[str]) -> StateRet:
    """ Only called if previous char was *. Dumps ** if (current) char is *,
    else returns start_state

    Returns:
        Tuple of: next state, if state is complete, if read next char, if append char
    """

    if char == '*':
        stack.append(char)
        return StateRet(operator_state, True, True)

    if char == '+':
        return StateRet(plus_post_operator_state, True, False)

    if char == '-':
        return StateRet(minus_post_operator_state, True, False)

    if char in ['/', ')', '%']:
        raise Exception("Illegal combination: *{}".format(char))

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
        return StateRet(operator_state, True, True)

    if char == '+':
        return StateRet(plus_post_operator_state, True, False)

    if char == '-':
        return StateRet(minus_post_operator_state, True, False)

    if char in ['*', ')', '%']:
        raise Exception("Illegal combination: /{}".format(char))

    else:
        return StateRet(start_state, True, False)


def artificial_mul_state(char: str, stack: List[str]) -> StateRet:

    stack.append('*')
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

        print(char, state.__name__, stack)

        if return_state.increment:
            idx += 1

        if return_state.done:
            append_token(stack, state, output_list)
            stack = []

        if idx == len(input_string):
            if not return_state.done:
                if stack[-1].isdigit() or stack[-1] == ")":
                    append_token(stack, return_state.next_state, output_list)
                else:
                    raise Exception('Ending expression with non-digit nor right parenthesis')
            break

        state = return_state.next_state

    return output_list



if __name__ == '__main__':

    #input_string = 'cos(2+-2)'
    input_string = "2-+-+-2"

    print([token['name'] for token in tokenizer(input_string)])
