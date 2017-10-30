from typing import List, Callable, Tuple, Any, Dict, Optional
from collections import namedtuple
import logging
import re
import string


from .settings import MATH_SYMBOLS, OPERATOR_LIST

# TODO: DOT STATE AFTER OPERATOR STATE

StateRet = namedtuple('StateRet', ['next_state', 'append', 'done', 'increment'])


from functools import wraps

class PythonSyntaxError(SyntaxError):
    """Docs."""


def generic_state(
        char,
        illegal_chars: Optional[Tuple[str]] = None,
        mapping: [Dict[str, Tuple[Any]]] = None,
):
    #logger = logging.getLogger(__name__)
    #logger.debug(f'in state {}; processing {char}')

    print(char)

    if illegal_chars is not None and char in illegal_chars:
        raise Exception('wrong')
        #raise PythonSyntaxError(f'Illegal combination: {char}')

    if char in mapping:
        return StateRet(*mapping[char])


def start_state(char: str, stack: List[str]) -> StateRet:
    """Start state.

    Called when reading the first character or when a state that has
    no restriction on the proceeding character.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Call to generic state with char, illegal chars, and mapping from char to:
        next state, if append char, if state is done, if increment
    """

    del stack # Not used in this state

    return generic_state(
        char,
        illegal_chars=',',
        mapping={
            **{str(digit): (num_pre_dot_state, True, False, True) for digit in string.digits},
            **{str(sym): (sym_state, False, False, False) for sym in MATH_SYMBOLS},
            **{str(letter): (func_state, True, False, True) for letter in string.ascii_letters},
            '.': (num_post_dot_state, True, False, True)
        },
    )



def func_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing word characters.

    Appends word-characters to stack.
    Completes when reaching '('.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Call to generic state with char, illegal chars, and mapping from char to:
        next state, if append char, if state is done, if increment
    """

    del stack # Not used in this state

    return generic_state(
        char,
        illegal_chars=(
            *(str(sym) for sym in MATH_SYMBOLS if sym != '('),
            *(str(digit) for digit in string.digits),
            '.',
            ','
        ),
        mapping={
            **{str(letter): (func_state, True, False, True) for letter in string.ascii_letters},
            '(': (post_func_state, False, True, False)
        }
    )


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

    del stack # Not used in this state

    return StateRet(left_parenthesis_state, True, True, True)


def num_pre_dot_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing numerical characters.

    Appends digits to stack.
    Switches to num_post_dot_state is char is '.'.
    Dumps char to stack when reaching a math symbol / operator.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Call to generic state with char, illegal chars, and mapping from char to:
        next state, if append char, if state is done, if increment
    """

    del stack # Not used in this state

    return generic_state(
        char,
        illegal_chars= (
            '(',
            *(str(letter) for letter in string.ascii_letters),
        ),
        mapping={
            **{str(digit): (num_pre_dot_state, True, False, True) for digit in string.digits},
            **{str(sym): (sym_state, False, True, False) for sym in MATH_SYMBOLS if sym != '('},
            ',': (comma_state, False, True, False),
            '.': (num_post_dot_state, True, False, True)
        },
    )




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
        Call to generic state with char, illegal chars, and mapping from char to:
        next state, if append char, if state is done, if increment
    """

    del stack # Not used in this state

    return generic_state(
        char,
        illegal_chars= (
            '(',
            *(str(letter) for letter in string.ascii_letters),
            '.'
        ),
        mapping={
            **{str(digit): (num_post_dot_state, True, False, True) for digit in string.digits},
            **{str(sym): (sym_state, False, True, False) for sym in MATH_SYMBOLS if sym != '('},
            ',': (comma_state, False, True, False),
        },
    )



def sym_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing mathematical symbols / operators.

    Appends mathematical symbols / operator to stack and
    directs to respective states.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Call to generic state with char, illegal chars, and mapping from char to:
        next state, if append char, if state is done, if increment
    """

    del stack # Not used in this state

    return generic_state(
        char,
        illegal_chars= None,
        mapping = {
            '(': (left_parenthesis_state, True, True, True),
            ')': (right_parenthesis_state, True, True, True),
            '%': (operator_state, True, True, True),
            '-': (minus_state, True, False, True),
            '+': (plus_state, True, False, True),
            '*': (mul_state, True, False, True),
            '/': (div_state, True, False, True)
        },
    )


def left_parenthesis_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing characters after '('.

    Only called after sym_state. Raises exception if the next
    char is a non-additive operator.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Call to generic state with char, illegal chars, and mapping from char to:
        next state, if append char, if state is done, if increment
    """

    del stack # Not used in this state

    return generic_state(
        char,
        illegal_chars = (
            *(str(sym) for sym in MATH_SYMBOLS if sym not in ['+', '-', '(']),
            ','
        ),
        mapping = {
            '+': (plus_post_operator_state, False, False, False),
            '-': (minus_post_operator_state, False, False, False),
            '(': (left_parenthesis_state, True, True, True),
            **{str(digit): (num_pre_dot_state, False, True, False) for digit in string.digits},
            **{str(letter): (func_state, False, True, False) for letter in string.ascii_letters},
            '.': (num_pre_dot_state, False, True, False),

        },
    )


def right_parenthesis_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing characters after ')'.

    Called after sym_state. Raises exception if the next
    char is a number or a letter (e.g., operator).

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Call to generic state with char, illegal chars, and mapping from char to:
        next state, if append char, if state is done, if increment
    """

    del stack # Not used in this state

    return generic_state(
        char,
        illegal_chars = (
            *(str(digit) for digit in string.digits),
            *(str(letter) for letter in string.ascii_letters),
            '(',
            ',',
            '.'
        ),
        mapping = {
            **{str(sym): (sym_state, False, False, False) for sym in MATH_SYMBOLS if sym != '('},
        },
    )


def operator_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing characters after (non-additive) operators.

    Raises:
        Exception if char is an additive operator or ')'.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Call to generic state with char, illegal chars, and mapping from char to:
        next state, if append char, if state is done, if increment
    """

    del stack # Not used in this state

    return generic_state(
        char,
        illegal_chars = (
            *(str(sym) for sym in MATH_SYMBOLS if sym not in ['+', '-', '(']),
            ',',
        ),
        mapping = {
            **{str(letter): (func_state, False, True, False) for letter in string.ascii_letters},
            **{str(digit): (num_pre_dot_state, False, True, False) for digit in string.digits},
            '(': (left_parenthesis_state, False, True, False),
            '+': (plus_post_operator_state, False, False, False),
            '-': (minus_post_operator_state, False, False, False),
            '.': (num_pre_dot_state, False, True, False)
        },
    )


def plus_state(char: str, stack: List[str]) -> StateRet:
    """Rules for tokenizing characters after '+'.

    Replaces '+' to '-' if char is '-'.

    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.

    Returns:
        Call to generic state with char, illegal chars, and mapping from char to:
        next state, if append char, if state is done, if increment
    """

    if char == '-':
        stack.pop()
        return StateRet(minus_state, True, False, True)

    return generic_state(
            char,
            illegal_chars = (
                *(str(sym) for sym in MATH_SYMBOLS if sym not in ['+', '-', '(']),
                ',',
            ),
            mapping = {
                **{str(letter): (func_state, False, True, False) for letter in string.ascii_letters},
                **{str(digit): (num_pre_dot_state, False, True, False) for digit in string.digits},
                '(': (left_parenthesis_state, False, True, False),
                '+': (plus_state, False, False, True),
                '.': (num_pre_dot_state, False, True, False)
            },
        )


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

    return generic_state(
        char,
        defaults=(start_state, False, True),
        mapping={
            '+': (minus_state, False, True),
        },
        illegal_chars=set(MATH_SYMBOLS).difference(('(')),
    )


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
        append_to_stack = True

    else:
        append_to_stack = None

    return generic_state(
        char,
        defaults=(start_state, True, False),
        mapping={
            '*': (operator_state, True, True),
            '+': (plus_post_operator_state, True, False),
            '-': (minus_post_operator_state, True, False),
        },
        illegal_chars=set(MATH_SYMBOLS).difference(('(')),
        append_to_stack=append_to_stack
    )


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
        append_to_stack = True

    else:
        append_to_stack = None

    return generic_state(
        char,
        defaults=(start_state, True, False),
        mapping={
            "/": (operator_state, True, True),
            "+": (plus_post_operator_state, True, False),
            "-": (minus_post_operator_state, True, False),
        },
        illegal_chars=set(MATH_SYMBOLS).difference(('(')),
        append_to_stack = append_to_stack
    )


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

