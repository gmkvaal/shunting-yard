from tokenizer_FSM import MATH_SYMBOLS, start_state, word_state, num_pre_dot_state, num_post_dot_state, sym_state
import pytest


def test_start_state():

    stack = []
    for i, char in enumerate("aAzZ"):
        return_state = start_state(char, stack)
        assert return_state  == (word_state, False, True)
        assert stack[i] == char

    for char in MATH_SYMBOLS:
        return_state = start_state(char, stack)
        assert return_state == (sym_state, False, False)

    stack = []
    for i, char in enumerate(map(str, range(0, 9))):
        return_state = start_state(char, stack)
        assert return_state == (num_pre_dot_state, False, True)
        #assert stack[i] == char

    char = '.'
    return_state = start_state(char, stack)
    assert return_state == (num_post_dot_state, False, True)

"""
def test_word_state():

    stack = []
    for char in "aAzZ":
        return_state = word_state(char, stack)
        assert return_state  == (word_state, False, True)
"""


def test_pre_num_state():

    stack = []
    for char in map(str, range(0,9)):
        return_state = num_pre_dot_state(char, stack)
        assert return_state  == (num_pre_dot_state, False, True)

    for char in '.':
        return_state = num_pre_dot_state(char, stack)
        assert return_state == (num_post_dot_state, False, True)

    for char in MATH_SYMBOLS:
        return_state = num_pre_dot_state(char, stack)
        assert return_state == (sym_state, True, False)

    for char in "aAzZ":
        with pytest.raises(Exception) as excinfo:
            num_pre_dot_state(char, stack)
        assert str(excinfo.value) == "Missing operator between number and letter: {}{}".format(''.join(stack), char)


def test_pre_num_state():

    stack = []
    for char in map(str, range(0,9)):
        return_state = num_post_dot_state(char, stack)
        assert return_state  == (num_post_dot_state, False, True)

    for char in '.':
        with pytest.raises(Exception) as excinfo:
            num_post_dot_state(char, stack)
        assert str(excinfo.value) == "Too many dots: {}.". format(''.join(stack))

    for char in MATH_SYMBOLS:
        return_state = num_post_dot_state(char, stack)
        assert return_state == (sym_state, True, False)

    for char in "aAzZ":
        with pytest.raises(Exception) as excinfo:
            num_post_dot_state(char, stack)
        assert str(excinfo.value) == "Missing operator between number and letter: {}{}".format(''.join(stack), char)

