from shunting_yard import classify_token, number, operator, pop_operators
from parser_FSM import tokenizer


OPERATOR_STACK_0 = []


# DANGEROUS GLOBAL VARIABLE
OPERATOR_STACK_1 = [
                      {
                       'name': '**',
                       'value': None,
                       'type': 'OPERATOR',
                       'precedence': 1, ''
                       'associativity': 'LEFT'
                       },
                      {
                       'name': '/',
                       'value': None,
                       'type': 'OPERATOR',
                       'precedence': 3,
                       'associativity': 'LEFT'
                       },
                       {
                        'name': '*',
                        'value': None,
                        'type': 'OPERATOR',
                        'precedence': 3,
                        'associativity': 'LEFT'
                        }
]


def test_operator():

    token = {
            'name': '*',
            'value': None,
            'type': 'OPERATOR',
            'precedence': 4,
            'associativity': 'LEFT'
     }

    output_queue = []

    return_state = operator(token, OPERATOR_STACK_1, output_queue)
    assert return_state == (pop_operators, False)

    return_state = operator(token, OPERATOR_STACK_0, output_queue)
    assert return_state == (classify_token, True)


def test_pop_operators_1():

    token = {
            'name': '/',
            'value': None,
            'type': 'OPERATOR',
            'precedence': 3,
            'associativity': 'LEFT'
     }

    output_queue = []

    return_state = pop_operators(token, OPERATOR_STACK_1, output_queue)
    assert return_state == (pop_operators, False)
    assert output_queue[-1] == {
                        'name': '*',
                        'value': None,
                        'type': 'OPERATOR',
                        'precedence': 3,
                        'associativity': 'LEFT'
                        }


def test_pop_operators_2():

    token = {
            'name': '+',
            'value': None,
            'type': 'OPERATOR',
            'precedence': 4,
            'associativity': 'LEFT'
     }

    output_queue = []

    return_state = pop_operators(token, OPERATOR_STACK_1, output_queue)
    assert return_state == (classify_token, True)
    assert OPERATOR_STACK_1[-1] == token