from typing import List, Callable, Any, Dict

from .settings import OPERATOR_LIST, OPERATOR_PRECEDENCE, OPERATOR_ASSOCIATIVITY

# TODO: SIMPLER AND STRONGER METHOD FOR TYPE CHARACHTERIZATION

def append_token(stack: List[str], state: Callable[[str, List[str]], Any],  output_list: List[Dict[str, Any]]) -> None:

    token  = ''.join(stack)

    if state.__name__ in ('num_pre_dot_state',
                          'num_post_dot_state'
                          ):

        token_value = float(token)
        token_type = 'NUMBER'

    elif state.__name__ in ('sym_state',
                            'div_state',
                            'mul_state',
                            'comma_state',
                            'plus_state',
                            'minus_state',
                            'plus_post_operator_state',
                            'minus_post_operator_state',
                            'artificial_mul_state',
                            'operator_state',
                            'leave_minus_post_operator_state',
                            'post_func_state'
                            ):

        token_value = None

        if token == '(':
            token_type = 'LEFT_PARENTHESIS'

        elif token == ')':
            token_type = 'RIGHT_PARENTHESIS'

        else:
            token_type = 'OPERATOR'

    elif state.__name__ == 'func_state':

        token_value = None

        if token in OPERATOR_LIST:
            token_type = 'OPERATOR'
        else:
            raise Exception('Undefined operator: {}'.format(token))

    else:
        raise Exception('Unknown state: {}'. format(state))

    if token in OPERATOR_PRECEDENCE.keys():
        precedence = OPERATOR_PRECEDENCE[token]

    else:
        precedence = None

    if token in OPERATOR_ASSOCIATIVITY.keys():
        associativity = OPERATOR_ASSOCIATIVITY[token]

    else:
        associativity = None

    output_list.append(
        {'name': token,
         'value': token_value,
         'type': token_type,
         'precedence': precedence,
         'associativity': associativity
        }
    )

if __name__ == '__main__':
    from tokenizer_FSM import num_post_dot_state

    output_list = []
    stack = ['1', '.', '2']
    token_type = "NUMBER"

    append_token(stack, num_post_dot_state, output_list)
    print(output_list)
