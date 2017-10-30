import pytest

from shunting_yard.states import (
    start_state, func_state, post_func_state, num_pre_dot_state,
    num_post_dot_state, sym_state, mul_state, div_state, comma_state,
    left_parenthesis_state, right_parenthesis_state, operator_state,
    plus_state, minus_state, plus_post_operator_state, minus_post_operator_state,
    minus_minus_post_operator_state, leave_minus_post_operator_state,
    PythonSyntaxError,
)
    

from shunting_yard.settings import OPERATOR_LIST, MATH_SYMBOLS

"""
def test_tokenizer():

    input_string = "cos(3)"
    correct_answer = ['1', '**', '-', 'max', '(', '4', ',', '2', ')', '*', 'cos', '(', '3', ')' ]
    output_list = tokenizer(input_string)
    assert output_list == correct_answer
"""

def test_start_state():

    stack = []
    for i, char in enumerate("aAzZ"):
        return_state = start_state(char, stack)
        assert return_state  == (func_state, True,  False, True)
        #assert stack[i] == char

    for char in MATH_SYMBOLS:
        return_state = start_state(char, stack)
        assert return_state == (sym_state, False, False, False)

    stack = []
    for i, char in enumerate(map(str, range(0, 9))):
        return_state = start_state(char, stack)
        assert return_state == (num_pre_dot_state, True, False, True)
        #assert stack[i] == char

    char = '.'
    return_state = start_state(char, stack)
    assert return_state == (num_post_dot_state, True, False, True)

    stack = []
    for char in {'#%,'}:
        with pytest.raises(Exception) as excinfo:
            start_state(char, stack)
            assert (str(excinfo.value) == 'Illegal character or illegal '
                                          'character placement:{}'.format(char))


def test_func_state():

    stack = []
    for i, char in enumerate("aAzZ"):
        return_state = func_state(char, stack)
        assert return_state  == (func_state, True, False, True)
        #stack[i] = char

    for char in ['1', '+', '*', '.']:
        with pytest.raises(Exception) as excinfo:
            return_state = func_state(char, stack)

    char = '('
    return_state = func_state(char, stack)
    assert return_state == (post_func_state, False, True, False)



def test_post_func_state():

    stack = []
    char = '('
    return_state = post_func_state(char, stack)
    assert return_state == (left_parenthesis_state, True, True, True)


def test_pre_num_state():

    stack = []
    for i, char in enumerate(map(str, range(0,9))):
        return_state = num_pre_dot_state(char, stack)
        assert return_state  == (num_pre_dot_state, True, False, True)
        #assert stack[i] == char

    stack = []
    for char in '.':
        return_state = num_pre_dot_state(char, stack)
        assert return_state == (num_post_dot_state, True, False, True)
        #assert stack[-1] == char

    char = ','
    return_state = num_pre_dot_state(char, stack)
    assert return_state == (comma_state, False, True, False)

    for char in MATH_SYMBOLS:
        if char != '(':
            return_state = num_pre_dot_state(char, stack)
            assert return_state == (sym_state, False, True, False)

    for char in "aAzZ(":
        with pytest.raises(Exception) as excinfo:
            num_pre_dot_state(char, stack)


def test_post_num_state():

    stack = []
    for i, char in enumerate(map(str, range(0, 9))):
        return_state = num_post_dot_state(char, stack)
        assert return_state  == (num_post_dot_state, True, False, True)

    char = '.'
    with pytest.raises(Exception) as excinfo:
        num_post_dot_state(char, stack)

    char = ','
    return_state = num_pre_dot_state(char, stack)
    assert return_state == (comma_state, False, True, False)

    stack = []
    for char in MATH_SYMBOLS:
        if char != '(':
            return_state = num_post_dot_state(char, stack)
            assert return_state == (sym_state, False, True, False)

    for char in "aAzZ(":
        with pytest.raises(Exception) as excinfo:
            num_pre_dot_state(char, stack)


def test_sym_state():

    stack = []
    char = '('
    return_state = sym_state(char, stack)
    assert return_state == (left_parenthesis_state, True, True, True)
    #assert stack[-1] == char

    stack = []
    char = ')'
    return_state = sym_state(char, stack)
    assert return_state  == (right_parenthesis_state, True, True, True)
    #assert stack[-1] == char

    stack = []
    char = '%'
    return_state = sym_state(char, stack)
    assert return_state == (operator_state, True, True, True)
    #assert stack[-1] == char

    stack = []
    char = '+'
    return_state = sym_state(char, stack)
    assert return_state == (plus_state, True, False, True)
    #assert stack[-1] == char

    stack = []
    char = '-'
    return_state = sym_state(char, stack)
    assert return_state == (minus_state, True, False, True)
    #assert stack[-1] == char

    stack = []
    char = '*'
    return_state = sym_state(char, stack)
    assert return_state == (mul_state, True, False, True)
    #assert stack[-1] == char

    stack = []
    char = '/'
    return_state = sym_state(char, stack)
    assert return_state == (div_state, True, False, True)
    #assert stack[-1] == char


def test_left_parenthesis_state():

    stack = []
    for char in MATH_SYMBOLS:
        if char not in ['+', '-', '(']:
            with pytest.raises(Exception) as excinfo:
                left_parenthesis_state(char, stack)

    stack = []
    char = '+'
    return_state = left_parenthesis_state(char, stack)
    assert return_state == (plus_post_operator_state, False, False, False)


    stack = []
    char = '-'
    return_state = left_parenthesis_state(char, stack)
    assert return_state == (minus_post_operator_state, False, False, False)
    #assert len(stack) == 0

    stack = []
    for char in "aAzZ":
        return_state = left_parenthesis_state(char, stack)
        assert return_state == (func_state, False, True, False)

    for char in "123456789.":
        return_state = left_parenthesis_state(char, stack)
        assert return_state == (num_pre_dot_state, False, True, False)


def test_right_parenthesis_state():

    stack = []
    for char in 'aAzZ1.,(':
        with pytest.raises(Exception) as excinfo:
            return_state = right_parenthesis_state(char, stack)

    stack = []
    for char in MATH_SYMBOLS:
        if char != '(':
            return_state = right_parenthesis_state(char, stack)
            assert return_state == (sym_state, False, False, False)




def test_operator_state():

    stack = []
    for char in MATH_SYMBOLS:
        if char not in ['+', '-', '(']:
            with pytest.raises(Exception) as excinfo:
                operator_state(char, stack)

    stack = []
    char = '+'
    return_state = operator_state(char, stack)
    assert return_state == (plus_post_operator_state, False, True, False)
    assert len(stack) == 0

    stack = []
    char = '-'
    return_state = operator_state(char, stack)
    assert return_state == (minus_post_operator_state, False, True, False)
    assert len(stack) == 0

    stack = []
    char = '('
    return_state = operator_state(char, stack)
    assert return_state == (left_parenthesis_state, False, True, False)
    assert len(stack) == 0

    for char in 'aAzZ':
        return_state = operator_state(char, stack)
        assert return_state == (func_state, False, True, False)
        assert len(stack) == 0

    for char in '12345':
        return_state = operator_state(char, stack)
        assert return_state == (num_pre_dot_state, False, True, False)
        assert len(stack) == 0



def test_plus_state():

    stack = []
    char = '+'
    return_state = plus_state(char, stack)
    assert return_state == (plus_state, False, False, True)
    #assert len(stack) == 0

    stack = ['-']
    char = '-'
    return_state = plus_state(char, stack)
    assert return_state == (minus_state, True, False, True)
    #assert stack[-1] == char

    stack = []
    char = '('
    return_state = plus_state(char, stack)
    assert return_state == (left_parenthesis_state, False, True, False)

    stack = []
    for char in MATH_SYMBOLS:
        if char not in ['+', '-', '(']:
            with pytest.raises(Exception) as excinfo:
                plus_state(char, stack)

    for char in "aAzZ":
        return_state = plus_state(char, stack)
        assert return_state == (func_state, False, True, False)

    for char in "1234567890.":
        return_state = plus_state(char, stack)
        assert return_state == (num_pre_dot_state, False, True, False)


def test_minus_state():

    stack = []
    char = '+'
    return_state = minus_state(char, stack)
    assert return_state == (minus_state, False, False, True)
    assert len(stack) == 0

    stack = ['-']
    char = '-'
    return_state = minus_state(char, stack)
    assert return_state == (plus_state, False, False, True)
    assert stack[-1] == '+'

    stack = []
    for char in "aAzZ":
        return_state = plus_state(char, stack)
        assert return_state == (func_state, False, True, False)

    for char in "1234567890.":
        return_state = plus_state(char, stack)
        assert return_state == (num_pre_dot_state, False, True, False)


def test_plus_post_operator_state():

    stack = []
    char = '+'
    return_state = plus_post_operator_state(char, stack)
    assert return_state == (plus_post_operator_state, False, False, True)
    #assert len(stack) == 0

    stack = []
    char = '-'
    return_state = plus_post_operator_state(char, stack)
    assert return_state == (minus_post_operator_state, False, False, True)
    assert len(stack) == 0

    stack = []
    for char in "aAzZ":
        return_state = plus_post_operator_state(char, stack)
        assert return_state == (func_state, False, False, False)

    for char in "1234567890.":
        return_state = plus_post_operator_state(char, stack)
        assert return_state == (num_pre_dot_state, False, False, False)


def test_minus_post_operator_state():

    stack = []
    char = '+'
    return_state = minus_post_operator_state(char, stack)
    assert return_state == (minus_post_operator_state, False, False, True)
    #assert len(stack) == 0

    stack = []
    char = '-'
    return_state = minus_post_operator_state(char, stack)
    assert return_state == (minus_minus_post_operator_state, False, False, True)
    assert len(stack) == 0

    stack = []
    for char in MATH_SYMBOLS:
        if char not in ['+', '-', '(']:
            with pytest.raises(Exception) as excinfo:
                minus_post_operator_state(char, stack)

    stack = []
    for char in "aAzZ":
        return_state = minus_post_operator_state(char, stack)
        assert return_state == (leave_minus_post_operator_state, False, False, False)

    for char in "1234567890.":
        return_state = minus_post_operator_state(char, stack)
        assert return_state == (leave_minus_post_operator_state, False, False, False)


def test_minus_minus_post_operator_state():

    stack = []
    char = '-'
    return_state = minus_minus_post_operator_state(char, stack)
    assert return_state == (plus_post_operator_state, True, False, True)

    stack = ['-']
    char = '-'
    return_state = minus_minus_post_operator_state(char, stack)
    assert return_state == (plus_post_operator_state, False, False, True)


def test_mul_state():

    stack = ['*']
    char = '*'
    return_state = mul_state(char, stack)
    assert return_state  == (operator_state, True, True, True)
    #assert stack == ['*', '*']

    for char in MATH_SYMBOLS:
        if char not in ['+', '-', '*', '(']:
            with pytest.raises(Exception) as excinfo:
                mul_state(char, stack)

    for char in "aAzZ":
        return_state = mul_state(char, stack)
        assert return_state == (func_state, False, True, False)

    for char in "1.":
        return_state = mul_state(char, stack)
        assert return_state == (num_pre_dot_state, False, True, False)


def test_div_state():

    stack = ['/']
    char = '/'
    return_state = div_state(char, stack)
    assert return_state  == (operator_state, True, True, True)
    #assert stack == ['*', '*']

    #stack = []
    for char in MATH_SYMBOLS:
        if char not in ['+', '-', '/', '(']:
            with pytest.raises(Exception) as excinfo:
                div_state(char, stack)

    #stack = []
    for char in "aAzZ":
        return_state = div_state(char, stack)
        assert return_state == (func_state, False, True, False)
        #assert stack == []

    #stack = []
    for char in "1.":
        return_state = div_state(char, stack)
        assert return_state == (num_pre_dot_state, False, True, False)
        #assert stack == []

