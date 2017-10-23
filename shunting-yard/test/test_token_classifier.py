from tokenizer_FSM import word_state, num_pre_dot_state, \
    num_post_dot_state, sym_state, mul_state, div_state, comma_state, tokenizer
from token_classifier import append_token
import pytest


def test_append_operator():

    state = word_state
    stack = ['c', 'o', 's']
    output_list = []

    append_token(stack, state, output_list)

    assert output_list == [{'name': 'cos', 'value': None, 'type': 'OPERATOR'}]


def test_append_unknown_operator():

    state = word_state
    stack = ['w', 'r', 'o', 'n', 'g']
    output_list = []

    with pytest.raises(Exception) as excinfo:
        append_token(stack, state, output_list)


def test_append_dot_number():

    state = num_pre_dot_state
    stack = ['1', '.', '2']
    output_list = []

    append_token(stack, state, output_list)

    assert output_list == [{'name': '1.2', 'value': 1.2, 'type': 'NUMBER'}]


def test_append_pre_dot_number():

    state = num_post_dot_state
    stack = ['1']
    output_list = []

    append_token(stack, state, output_list)

    assert output_list == [{'name': '1', 'value': 1, 'type': 'NUMBER'}]


def test_append_sym_state():

    state = sym_state
    stack = ['+']
    output_list = []

    append_token(stack, state, output_list)

    assert output_list == [{'name': '+', 'value': None, 'type': 'OPERATOR'}]