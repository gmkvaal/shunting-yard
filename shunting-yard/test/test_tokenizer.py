from tokenizer_FSM import MATH_SYMBOLS, start_state, word_state, num_pre_dot_state, \
    num_post_dot_state, sym_state, mul_state, div_state, comma_state
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

    stack = []
    for char in {'#%,'}:
        with pytest.raises(Exception) as excinfo:
            start_state(char, stack)
            assert (str(excinfo.value) == 'Illegal character or illegal '
                                          'character placement:{}'.format(char))


def test_word_state():

    stack = []
    for char in "aAzZ":
        return_state = word_state(char, stack)
        assert return_state  == (word_state, False, True)

    for char in MATH_SYMBOLS:
        return_state = word_state(char, stack)
        assert return_state == (start_state, True, False)

    char = ','
    return_state = word_state(char, stack)
    assert return_state == (comma_state, True, False)

    for char in ['1']:
        return_state = word_state(char, stack)
        assert return_state == (start_state, True, False)


def test_pre_num_state():

    stack = []
    for i, char in enumerate(map(str, range(0,9))):
        return_state = num_pre_dot_state(char, stack)
        assert return_state  == (num_pre_dot_state, False, True)
        assert stack[i] == char

    stack = []
    for char in '.':
        return_state = num_pre_dot_state(char, stack)
        assert return_state == (num_post_dot_state, False, True)
        assert stack[-1] == char

    char = ','
    return_state = num_pre_dot_state(char, stack)
    assert return_state == (comma_state, True, False)

    for char in MATH_SYMBOLS:
        return_state = num_pre_dot_state(char, stack)
        assert return_state == (sym_state, True, False)

    for char in "aAzZ":
        with pytest.raises(Exception) as excinfo:
            num_pre_dot_state(char, stack)
            assert (str(excinfo.value) == "Missing operator between number and letter: "
                                      "{}{}".format(''.join(stack), char))


def test_post_num_state():

    stack = []
    for i, char in enumerate(map(str, range(0, 9))):
        return_state = num_post_dot_state(char, stack)
        assert return_state  == (num_post_dot_state, False, True)
        assert stack[i] == char

    char = '.'
    with pytest.raises(Exception) as excinfo:
        num_post_dot_state(char, stack)
        assert str(excinfo.value) == "Too many dots: {}.". format(''.join(stack))

    char = ','
    return_state = num_pre_dot_state(char, stack)
    assert return_state == (comma_state, True, False)

    stack = []
    for char in MATH_SYMBOLS:
        return_state = num_post_dot_state(char, stack)
        assert return_state == (sym_state, True, False)
        assert stack == []

    for char in "aAzZ":
        with pytest.raises(Exception) as excinfo:
            num_post_dot_state(char, stack)
            assert (str(excinfo.value) == "Missing operator between number and letter: "
                                     "{}{}".format(''.join(stack), char))


def test_sym_state():

    stack = []
    for i, char in enumerate(['+', '-', '%', '(', ')']):
        return_state = sym_state(char, stack)
        assert return_state  == (start_state, True, True)
        assert stack[i] == char

    stack = []
    char = '*'
    return_state = sym_state(char, stack)
    assert return_state  == (mul_state, False, True)
    assert stack[-1] == char

    stack = []
    char = '/'
    return_state = sym_state(char, stack)
    assert return_state == (div_state, False, True)
    assert stack[-1] == char


def test_mul_state():

    stack = ['*']
    char = '*'
    return_state = mul_state(char, stack)
    assert return_state  == (start_state, True, True)
    assert stack == ['*', '*']

    stack = []
    for char in MATH_SYMBOLS:
        if char != '*':
            return_state = mul_state(char, stack)
            assert return_state == (start_state, True, False)
            assert stack == []

    stack = []
    for char in "aAzZ":
        return_state = mul_state(char, stack)
        assert return_state == (start_state, True, False)
        assert stack == []

    stack = []
    for char in "1.":
        return_state = mul_state(char, stack)
        assert return_state == (start_state, True, False)
        assert stack == []


def test_div_state():

    stack = ['/']
    char = '/'
    return_state = div_state(char, stack)
    assert return_state  == (start_state, True, True)
    assert stack == ['/', '/']

    stack = []
    for char in MATH_SYMBOLS:
        if char != '/':
            return_state = div_state(char, stack)
            assert return_state == (start_state, True, False)
            assert stack == []

    stack = []
    for char in "aAzZ":
        return_state = div_state(char, stack)
        assert return_state == (start_state, True, False)
        assert stack == []

    stack = []
    for char in "1.":
        return_state = div_state(char, stack)
        assert return_state == (start_state, True, False)
        assert stack == []