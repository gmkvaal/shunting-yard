from parser_finite_state import MATH_SYMBOLS, start_state, word_state, num_pre_dot_state, num_post_dot_state, sym_state

def test_start_state():

    stack = []
    for char in "aAzZ":
        return_state = start_state(char, stack)
        assert return_state  == (word_state, False, True, True)

    for char in MATH_SYMBOLS:
        return_state = start_state(char, stack)
        assert return_state == (sym_state, False, True, True)

    for char in map(str, range(0, 9)):
        return_state = start_state(char, stack)
        assert return_state == (num_pre_dot_state, False, True, True)

    char = '.'
    return_state = start_state(char, stack)
    assert return_state == (num_post_dot_state, False, True, True)

"""
def test_word_state():

    stack = []
    for char in "aAzZ":
        return_state = word_state(char, stack)
        assert return_state  == (word_state, False, True, True)
"""


def test_pre_num_state():

    stack = []
    for char in map(str, range(0,9)):
        return_state = num_pre_dot_state(char, stack)
        assert return_state  == (num_pre_dot_state, False, True, True)

    for char in '.':
        return_state = num_pre_dot_state(char, stack)
        assert return_state == (num_post_dot_state, False, True, True)



#def test_sym_state():
#
#    stack = []
#    for char in MATH_SYMBOLS:
#        return_state = sym_state(char, stack)
#        assert return_state  == (start_state, True, False)
