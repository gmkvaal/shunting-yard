from typing import List, Callable, Any, Dict
import string

from .settings import OPERATOR_LIST, OPERATOR_PRECEDENCE, OPERATOR_ASSOCIATIVITY, MATH_SYMBOLS


def append_token(stack: List[str], output_list: List[Dict[str, Any]]) -> None:

    token  = ''.join(stack)

    if token in MATH_SYMBOLS or OPERATOR_LIST:

        token_value = None
        token_type = 'OPERATOR'

        if token in OPERATOR_PRECEDENCE.keys():
            precedence = OPERATOR_PRECEDENCE[token]

        else:
            precedence = None

        if token in OPERATOR_ASSOCIATIVITY.keys():
            associativity = OPERATOR_ASSOCIATIVITY[token]

        else:
            associativity = None

    elif token[-1] in string.digits:

        token_value = float(token)
        token_type = 'NUMBER'
        precedence = None
        associativity = None

    else:
        print(token)
        print(MATH_SYMBOLS)
        raise Exception('Unknown type')

    output_list.append(
        {'name': token,
         'value': token_value,
         'type': token_type,
         'precedence': precedence,
         'associativity': associativity
        }
    )