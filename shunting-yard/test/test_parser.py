from parser import parser

def test_input_string1():
    """ Testing parser function """

    innstr = 'a+b+c'
    correct_output = ['a', '+', 'b', '+', 'c']
    output_list = parser(innstr)

    assert output_list == correct_output

def test_input_string1():
    """ Testing parser function """

    innstr = 'sin(a*b+cos(c))'
    correct_output = ['sin', '(', 'a', '*', 'b', '+', 'cos', '(', 'c', ')', ')']
    output_list = parser(innstr)

    assert output_list == correct_output