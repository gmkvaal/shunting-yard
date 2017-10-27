from typing import List
from collections import namedtuple
#from shunting_yard import settings
import re


StateRet = namedtuple('StateRet', ['next_state', 'done', 'increment'])


def start_state(char: str, stack: List[str]) -> StateRet:
    """Start state.

    Called when reading the first character or when a state that has
    no restriction on the proceeding character.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
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
        return StateRet(func_state, False, True)

    else:
        raise Exception('Illegal character or '
                        'illegal character placement:{}'.format(char))


def func_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing word characters.

    Appends word-characters to stack.
    Dumps char to stack when reaching (.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Raises:
         Exception if char is not alphabetical or (
    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    if re.match("([a-z]|[A-Z])", char):
        stack.append(char)
        return StateRet(func_state, False, True)

    elif char == '(':
        return StateRet(post_func_state, True, False)

    else:
        raise Exception('Illegal character {} after function'.format(char))


def post_func_state(char: str, stack: List[str]) -> StateRet:
    """Auxiliary function.

    Only called when func_state is successfully completed.
    Appends ( to the stack.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    stack.append(char)

    return StateRet(left_parenthesis_state, True, True)


def num_pre_dot_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing numerical characters.

    Appends digits to stack.
    Switches to num_post_dot_state is char is '.'.
    Dumps char to stack when reaching a math symbol / operator.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Raises:
         Exception if char is alphabetical or '('

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    if char.isdigit():
        stack.append(char)
        return StateRet(num_pre_dot_state, False, True)

    elif char == '.':
        stack.append(char)
        return StateRet(num_post_dot_state, False, True)

    elif char == ',':
        return StateRet(comma_state, True, False)

    elif char in MATH_SYMBOLS and char != '(':
        return StateRet(sym_state, True, False)

    else:
        raise Exception('Missing operator between: '
                        '{}{}'.format(''.join(stack), char))


def num_post_dot_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing numerical (decimal) characters.

    Only called after num_pre_dot_state.
    Dumps char to stack when reaching a math symbol / operator.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Raises:
         Exception if char is alphabetical or '('

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    if char.isdigit():
        stack.append(char)
        return StateRet(num_post_dot_state, False, True)

    elif char in MATH_SYMBOLS and char != '(':
        return StateRet(sym_state, True, False)

    elif char == ',':
        return StateRet(comma_state, True, False)

    elif char == '.':
        raise Exception('Too many dots: {}.'. format(''.join(stack)))

    else:
        raise Exception('Missing operator between: '
                        '{}{}'.format(''.join(stack), char))


def sym_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing mathematic symbols / operators.

    Appends mathematical symbols / operator to stack and
    directs to respective states.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
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
    """Rules for tokenizing characters after '('.

    Only called after sym_state. Raises exception if the next
    char is a non-additive operator.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Raises:
        Exception if char is a non-additive operator or ')'.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    if char in MATH_SYMBOLS and char not in ['+', '-', '(']:
        raise Exception('Non addidive operator after left parenthsis: '
                        '({}.'.format(char))

    if char == '+':
        return StateRet(plus_post_operator_state, False, False)

    if char == '-':
        return StateRet(minus_post_operator_state, False, False)

    else:
        return StateRet(start_state, False, False)


def right_parenthesis_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing characters after ')'.

    Called after sym_state. Raises exception if the next
    char is a number or a letter (e.g., operator).

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Raises:
        Exception if char is a number or a letter.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    if re.match('[0-9]', char):
        raise Exception('Missing operator between right parenthesis '
                        "and number: ){}".format(char))

    if re.match('([a-z]|[A-Z])', char):
        raise Exception('Missing operator between right parenthesis '
                        'and letter: ){}'.format(char))

    else:
        return StateRet(start_state, False, False)


def operator_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing characters after (non-additive) operators.

    Raises:
        Exception if char is an additive operator or ')'.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    if char in MATH_SYMBOLS and char not in ['(', '+', '-']:
        raise Exception('Operator after operator')

    if char == '+':
        return StateRet(plus_post_operator_state, False, False)

    if char == '-':
        return StateRet(minus_post_operator_state, False, False)

    else:
        return StateRet(start_state, False, False)


def plus_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing characters after '+'.

    Replaces '+' to '-' if char is '-'.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Raises:
        Exception if char is a non additive operator or ')'.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    if char == '+':
        return StateRet(plus_state, False, True)

    elif char == '-':
        stack.pop()
        stack.append(char)
        return StateRet(minus_state, False, True)

    elif char in MATH_SYMBOLS and char not in ['(', '+', '-']:
        raise Exception("Illegal combination of operators: +{}".format(char))

    else:
        return StateRet(start_state, True, False)


def minus_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing characters after '+'.

    Replaces '-' to '+' if char is '-'.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Raises:
        Exception if char is a non additive operator or ')'.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    if char == '-':
        stack.pop()
        stack.append('+')
        return StateRet(plus_state, False, True)

    elif char == '+':
        return StateRet(minus_state, False, True)

    elif char in MATH_SYMBOLS and char not in ['(', '+', '-']:
        raise Exception("Illegal combination of operators: {}"
                        "after additive operator".format(char))

    else:
        return StateRet(start_state, True, False)


def plus_post_operator_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing additive operators after non additives.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Raises:
        Exception if char is a non additive operator or ')'.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    if char == '+':
        return StateRet(plus_post_operator_state, False, True)

    elif char == '-':
        return StateRet(minus_post_operator_state, False, False)

    elif char in MATH_SYMBOLS and char not in ['(', '+', '-']:
        raise Exception('Illegal combination of operators: +{}'.format(char))

    else:
        return StateRet(start_state, False, False)


def minus_post_operator_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing additive operators after non additives.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Raises:
        Exception if char is a non additive operator or ')'.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    if char == '-':
        return StateRet(minus_minus_post_operator_state, False, False)

    elif char == '+':
        return StateRet(minus_post_operator_state, False, True)

    elif char in MATH_SYMBOLS and char not in ['(', '+', '-']:
        raise Exception("Illegal combination of operators: +{}".format(char))

    else:
        return StateRet(leave_minus_post_operator_state, False, False)


def leave_minus_post_operator_state(char: str, stack: List[str]) -> StateRet:
    """Auxiliary state

    Only called when successfully leaving minus_post_operator_state.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """
    if len(stack) == 0:
        pass

    elif stack[-1] == '-':
        stack.pop()

    return StateRet(negative_unary_state, False, False)


def negative_unary_state(char: str, stack: List[str]) -> StateRet:
    """Auxiliary state

    Adds the negative unary operator to the stack.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    stack.append('-u')
    return StateRet(start_state, True, False)


def minus_minus_post_operator_state(char: str, stack: List[str]) -> StateRet:
    """ Auxiliary state.

    Only called when an state is minus_post_operator_state and pointed
    character is '-'.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    if stack == []:
        stack.append(char)
        return StateRet(minus_post_operator_state, False, True)

    if stack[-1] == '-':
        stack.pop()
        return StateRet(plus_post_operator_state, False, True)


def mul_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing characters after '*'

    Dumps ** if char is *.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Raises:
        Exception if char is a non additive operator, ')' or '*'.

    Returns:
        Tuple of: next state, if state is complete, if read next charr.
    """

    if char == '*':
        stack.append(char)
        return StateRet(operator_state, True, True)

    if char == '+':
        return StateRet(plus_post_operator_state, True, False)

    if char == '-':
        return StateRet(minus_post_operator_state, True, False)

    if char in MATH_SYMBOLS and char not in ['+', '-', '*', '(']:
        raise Exception('Illegal combination: *{}'.format(char))

    else:
        return StateRet(start_state, True, False)


def div_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing characters after '*'

    Dumps // if char is /.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Raises:
        Exception if char is a non additive operator, ')' or '*'.

    Returns:
        Tuple of: next state, if state is complete, if read next char.
    """

    if char == '/':
        stack.append(char)
        return StateRet(operator_state, True, True)

    if char == '+':
        return StateRet(plus_post_operator_state, True, False)

    if char == '-':
        return StateRet(minus_post_operator_state, True, False)

    if char in MATH_SYMBOLS and char not in ['+', '-', '/', '(']:
        raise Exception('Illegal combination: /{}'.format(char))

    else:
        return StateRet(start_state, True, False)


def comma_state(char: str, stack: List[str]) -> StateRet:
    """Only called when char is comma

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Tuple of: next state, if state is complete, if read next char, if append char
    """

    stack.append(char)
    return StateRet(start_state, True, True)
