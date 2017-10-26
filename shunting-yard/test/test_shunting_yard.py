from shunting_yard import classify_token, operator, pop_operators
from parser_FSM import tokenizer




# DANGEROUS GLOBAL VARIABLE






def test_operator():

    operator_stack_1 = [
        {
            'name': '*',
            'value': None,
            'type': 'OPERATOR',
            'precedence': 3,
            'associativity': 'LEFT'
        }
    ]

    token = {
            'name': '*',
            'value': None,
            'type': 'OPERATOR',
            'precedence': 4,
            'associativity': 'LEFT'
     }

    output_queue = []

    return_state = operator(token, operator_stack_1, output_queue)
    assert return_state == (pop_operators, False)

    OPERATOR_STACK_0 = []

    return_state = operator(token, OPERATOR_STACK_0, output_queue)
    assert return_state == (classify_token, True)


def test_pop_operators_1():

    operator_stack_1 = [
        {
            'name': '*',
            'value': None,
            'type': 'OPERATOR',
            'precedence': 3,
            'associativity': 'LEFT'
        }
    ]

    token = {
            'name': '/',
            'value': None,
            'type': 'OPERATOR',
            'precedence': 3,
            'associativity': 'LEFT'
     }

    output_queue = []

    return_state = pop_operators(token, operator_stack_1, output_queue)
    assert return_state == (pop_operators, False)
    assert output_queue[-1] == {
                        'name': '*',
                        'value': None,
                        'type': 'OPERATOR',
                        'precedence': 3,
                        'associativity': 'LEFT'
                        }


def test_pop_operators_2():

    operator_stack_1 = [
        {
            'name': '*',
            'value': None,
            'type': 'OPERATOR',
            'precedence': 3,
            'associativity': 'LEFT'
        }
    ]


    token = {
            'name': '+',
            'value': None,
            'type': 'OPERATOR',
            'precedence': 4,
            'associativity': 'LEFT'
     }

    output_queue = []

    return_state = pop_operators(token, operator_stack_1, output_queue)
    assert return_state == (classify_token, True)
    assert operator_stack_1[-1] == token
