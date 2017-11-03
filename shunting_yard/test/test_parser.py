import pytest

from shunting_yard.parser import (classify_token, operator, pop_operators,
                                  right_parenthesis, post_right_parenthesis)
from shunting_yard.tokenizer import tokenizer


def test_classify_operator():

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

    return_state = classify_token(token, operator_stack_1, output_queue)
    assert return_state == (operator, False)
    assert output_queue == []


def test_classify_number():

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
            'name': '1',
            'value': 1.0,
            'type': 'NUMBER',
            'precedence': None,
            'associativity': None
     }

    output_queue = []

    return_state = classify_token(token, operator_stack_1, output_queue)
    assert return_state == (classify_token, True)
    assert output_queue[-1] == token


def test_classify_left_parenthesis():

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
            'name': '(',
            'value': None,
            'type': 'LEFT_PARENTHESIS',
            'precedence': None,
            'associativity': None
     }

    output_queue = []

    return_state = classify_token(token, operator_stack_1, output_queue)
    assert return_state == (classify_token, True)
    assert operator_stack_1[-1] == token


def test_classify_right_parenthesis():

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
            'name': ')',
            'value': None,
            'type': 'RIGHT_PARENTHESIS',
            'precedence': None,
            'associativity': None
     }

    output_queue = []

    return_state = classify_token(token, operator_stack_1, output_queue)
    assert return_state == (right_parenthesis, False)



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
            'name': '**',
            'value': None,
            'type': 'OPERATOR',
            'precedence': 1,
            'associativity': 'RIGHT'
     }

    output_queue = []

    return_state = operator(token, operator_stack_1, output_queue)
    assert return_state == (classify_token, True)
    assert operator_stack_1[-1] == token


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


def test_right_parenthesis():

    operator_stack = []

    token = {
            'name': ')',
            'value': None,
            'type': 'RIGHT_PARENTHESIS',
            'precedence': None,
            'associativity': None
    }

    output_queue = []

    with pytest.raises(Exception):
        right_parenthesis(token, operator_stack, output_queue)

    operator_stack = [
        {
            'name': '(',
            'value': None,
            'type': 'LEFT_PARENTHESIS',
            'precedence': None,
            'associativity': None
        }
    ]

    return_state = right_parenthesis(token, operator_stack, output_queue)
    assert return_state == (post_right_parenthesis, False)

    operator_stack = [
        {
            'name': '*',
            'value': None,
            'type': 'OPERATOR',
            'precedence': 3,
            'associativity': 'LEFT'
        }
    ]

    return_state = right_parenthesis(token, operator_stack, output_queue)
    assert return_state == (right_parenthesis, False)
