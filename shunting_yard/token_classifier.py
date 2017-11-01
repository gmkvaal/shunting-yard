from typing import List, Callable, Any, Dict
import string

from .error import PythonSyntaxError
from .settings import FUNCTION_LIST, OPERATOR_PRECEDENCE, OPERATOR_ASSOCIATIVITY, MATH_SYMBOLS


def append_token(stack: List[str], output_list: List[Dict[str, Any]]) -> None:
    """ Merges chars into tokens and appends to output_list
:
    Args:
        char: Current pointed character in the string.
        stack: List of characters to be merged into tokens.
    """

    token  = ''.join(stack)

    #print('token:', token)

    if token == '(':
        token_value = None
        token_type = 'LEFT_PARENTHESIS'
        precedence = None
        associativity = None

    elif token == ')':
        token_value = None
        token_type = 'RIGHT_PARENTHESIS'
        precedence = None
        associativity = None

    elif token in MATH_SYMBOLS:
        token_value = None
        token_type = 'OPERATOR'
        precedence = OPERATOR_PRECEDENCE[token]
        associativity = OPERATOR_ASSOCIATIVITY[token]

    elif token in FUNCTION_LIST:
        token_value = None
        token_type = 'FUNCTION'
        precedence = None
        associativity = None

    elif token[-1] in string.digits:
        token_value = float(token)
        token_type = 'NUMBER'
        precedence = None
        associativity = None

    elif token == ',':
        token_value = None
        token_type = 'SKIP'
        precedence = None
        associativity = None

    else:
        print(token)
        raise PythonSyntaxError(f'Unable to classify token: {token}')

    output_list.append(
        {'name': token,
         'value': token_value,
         'type': token_type,
         'precedence': precedence,
         'associativity': associativity
        }
    )