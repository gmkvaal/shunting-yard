import pytest

from shunting_yard.token_classifier import append_token, MATH_SYMBOLS


def test_append_operator():

    stack = ['c', 'o', 's']
    output_list = []

    append_token(stack, output_list)

    assert output_list == [{'name': 'cos', 'value': None, 'type': 'FUNCTION',
                            'precedence': None, 'associativity': None}]


def test_append_unknown_operator():

    stack = ['w', 'r', 'o', 'n', 'g']
    output_list = []

    with pytest.raises(Exception) as excinfo:
        append_token(stack, output_list)


def test_append_math_symbols_1():

        stack = ['**']
        output_list = []

        append_token(stack, output_list)

        assert output_list == [{'name': '**', 'value': None, 'type': 'OPERATOR',
                                'precedence': 1, 'associativity': 'RIGHT'}]


def test_append_math_symbols_2():

    stack = ['-u']
    output_list = []

    append_token(stack, output_list)

    assert output_list == [{'name': '-u', 'value': None, 'type': 'OPERATOR',
                            'precedence': 2, 'associativity': 'RIGHT'}]


def test_append_math_symbols_3():

        stack = ['*']
        output_list = []

        append_token(stack, output_list)

        assert output_list == [{'name': '*', 'value': None, 'type': 'OPERATOR',
                                'precedence': 3, 'associativity': 'LEFT'}]


def test_append_number():

    stack = ['3.14']
    output_list = []

    append_token(stack, output_list)

    assert output_list == [{'name': '3.14', 'value': 3.14, 'type': 'NUMBER',
                            'precedence': None, 'associativity': None}]


def test_append_left_parenthesis():

    stack = ['(']
    output_list = []

    append_token(stack, output_list)

    assert output_list == [{'name': '(', 'value': None, 'type': 'LEFT_PARENTHESIS',
                            'precedence': None, 'associativity': None}]


def test_append_right_parenthesis():

    stack = [')']
    output_list = []

    append_token(stack, output_list)

    assert output_list == [{'name': ')', 'value': None, 'type': 'RIGHT_PARENTHESIS',
                            'precedence': None, 'associativity': None}]